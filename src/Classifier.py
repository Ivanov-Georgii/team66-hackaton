import re
from pathlib import Path
import shutil

class Classifier:
    def __init__(self):
        self.weights = {"ключевые сигналы": 2, "обычные сигналы": 1, "антисигналы": -1}
        self.minscore = 3
        self.pathCat = {
            "инциденты": Path("../SortedInbox/Incidence"),
            "автоответчики/noreply сообщения": Path("../SortedInbox/Noreply"),
            "спам": Path("../SortedInbox/Spam"),
            "вопросы/просьбы": Path("../SortedInbox/Questions"),
            "безопасность": Path("../SortedInbox/Sequrity"),
            "важное": Path("../SortedInbox/Important"),
            "прочее": Path("../SortedInbox/Other")
        }
        self.categories = {
            "инциденты": {
                "ключевые сигналы": ["ошибк", "баг", "сломал", "неработает", "упал", "сбой", "срочно"],
                "обычные сигналы": ["проблем", "завис", "незагружает", "неоткрывает", "недоступ", "падени"],
                "антисигналы": ["план", "обновлени", "релиз", "запланирован"]
            },
            "спам": {
                "ключевые сигналы": ["акци", "скидк", "бесплатно", "выиграл", "реклам"],
                "обычные сигналы": ["купить", "успей", "предложени", "распродаж", "инвестици", "заработ", "криптовалют",
                                    "биткоин"],
                "антисигналы": ["проект", "задач", "дедлайн", "отчет", "работ", "коллег", "встреч", "бизнес", "клиент",
                                "договор", "счет", "налог", "помоги", "вопрос", "ошибк", "баг"]
            },
            "вопросы/просьбы": {
                "ключевые сигналы": ["помоги", "подскажи", "помощь", "просьб"],
                "обычные сигналы": ["каксделать", "немогу", "неможем", "вопрос", "объясни", "чтоделать",
                                    "какбыть", "возможноли", "пожалуйста"],
                "антисигналы": ["срочно", "ошибк", "баг", "упал", "сломал"]
            },
            "автоответчики/noreply сообщения": {
                "ключевые сигналы": ["noreply", "autoreply", "автоответчик", "не отвечать"],
                "обычные сигналы": ["уведомлени", "нотификаци", "автоматическ", "сформирован", "создан", "сгенерирован",
                                    "notification", "заказ", "платеж","отчет", "доставлен", "отправлен", "получен"],
                "антисигналы": ["помоги", "срочно", "ответь"]
            },
            "безопасность": {
                "ключевые сигналы": ["парол", "взлом", "утечк", "фишинг"],
                "обычные сигналы": ["безопасность", "подозрительн", "несанкционированн", "доступ", "учетнаязапись",
                                    "вирус", "вредоносн"],
                "антисигналы": ["проект", "задач", "помоги", "вопрос", "отчет"]
            }
        }
        self.priorityCategories = ["спам", "автоответчики/noreply сообщения"]

    def extract_words(self, text: str) -> list:
        text = text.lower().replace('ё', 'е')
        text = text.lower().replace('не ', 'не')
        text = text.lower().replace('как ', 'как')
        text = text.lower().replace('что делать', 'чтоделать')
        text = text.lower().replace('возможно ли', 'возможноли')
        text = text.lower().replace('учетная запись', 'учетнаязапись')
        words = re.findall(r'[а-яa-z]{3,}', text)
        return list(words)

    def calculate_word_score(self, word: str, categoryName: str) -> int:
        categoryData = self.categories.get(categoryName, {})
        for signal in categoryData.get("ключевые сигналы", []):
            if signal in word:
                return self.weights["ключевые сигналы"]

        for signal in categoryData.get("обычные сигналы", []):
            if signal in word:
                return self.weights["обычные сигналы"]

        for signal in categoryData.get("антисигналы", []):
            if signal in word:
                return self.weights["антисигналы"]
        return 0

    def calculate_category_score(self, categoryName: str, subjectWords: list, bodyWords: list) -> int:
        score = 0
        for word in subjectWords:
            wordScore = self.calculate_word_score(word, categoryName)
            score += wordScore * 2
        for word in bodyWords:
            wordScore = self.calculate_word_score(word, categoryName)
            score += wordScore * 1
        return score

    def classify(self, subject: str = "", body: str = "", sender: str = "") -> str:
        subjectWords = self.extract_words(subject)
        bodyWords = self.extract_words(body)
        for priorityCategory in self.priorityCategories:
            if priorityCategory in self.categories:
                score = self.calculate_category_score(priorityCategory,subjectWords, bodyWords)
                if score >= self.minscore:
                    return priorityCategory

        scores = {}
        for categoryName in self.categories:
            if categoryName in self.priorityCategories:
                continue
            score = self.calculate_category_score(categoryName, subjectWords, bodyWords)
            if score > 0:
                scores[categoryName] = score
        if not scores:
            return "прочее"

        bestCategory = max(scores.keys(), key=lambda c: scores[c])
        bestScore = scores[bestCategory]
        if bestScore < self.minscore:
            return "прочее"
        return bestCategory

    def move_file_to_category(self, filePath: Path, categoryKey: str):
        targetFolder = self.pathCat.get(categoryKey, self.pathCat["прочее"])
        shutil.move(str(filePath), str(targetFolder))