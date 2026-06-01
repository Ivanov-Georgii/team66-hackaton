import re
from pathlib import Path
import shutil
import logging

class Classifier:
    def __init__(self):
        self.weights = {"ключевые сигналы": 2, "обычные сигналы": 1}
        self.minscore = 2
        self.pathCat = {
            "инциденты": Path("../SortedInbox/Incidents"),
            "автоответчики/noreply сообщения": Path("../SortedInbox/Noreply"),
            "спам": Path("../SortedInbox/Spam"),
            "вопросы/просьбы": Path("../SortedInbox/Questions"),
            "безопасность": Path("../SortedInbox/Security"),
            "важное": Path("../SortedInbox/Important"),
            "прочее": Path("../SortedInbox/Other")
        }
        self.categories = {
            "инциденты": {
                "ключевые сигналы": [
                    "инцидент", "сбой", "недоступ", "упал", "критич", "останов",
                    "авари", "краш", "срочно", "перегруз", "массов"
                ],
                "обычные сигналы": [
                    "останов", "неоткрыва", "неработа", "слома", "тормоз",
                    "незагружа", "неотвеча", "переустанов"
                ]
            },
            "спам": {
                "ключевые сигналы": [
                    "выиграл", "розыгрыш", "победит", "бесплатно", "акци",
                    "лотере", "приз", "фрибет", "казино", "игра"
                ],
                "обычные сигналы": [
                    "скидк", "реклам", "купить", "криптовалют", "биткоин",
                    "инвестици", "заработ", "распродаж", "промокод",
                    "эксклюзивн", "выгодн", "успе"
                ]
            },
            "вопросы/просьбы": {
                "ключевые сигналы": [
                    "прошу", "ремонт", "заявк", "выдат", "подскажи", "доступ",
                    "организ", "диагностик", "комп", "мышь", "клав", "включ",
                    "чтоделать", "возможноли", "какбыть", "кабел", "провод",
                    "антивирус", "windows", "винд", "зависает", "прос", "проблема",
                    "ноут", "экран", "монитор"
                ],
                "обычные сигналы": [
                    "помощь", "восстанов", "согласов", "инструкц", "вопрос",
                    "права", "рабочее", "подготов", "предостав", "уточни",
                    "пожалуйста", "немог", "объясни", "неработает", "неможет",
                    "[IT]"
                ]
            },
            "автоответчики/noreply сообщения": {
                "ключевые сигналы": [
                    "сгенерирован", "автоответ", "неотвечать", "рассылк"
                ],
                "обычные сигналы": [
                    "автоматическ", "уведомлени", "notification", "заказ",
                    "платеж", "доставлен", "отправлен", "получен", "сформирован"
                ]
            },
            "безопасность": {
                "ключевые сигналы": [
                    "фишинг", "взлом", "утечк", "верификац", "заблокир",
                    "мошенн", "угна", "укра", "вредоносн", "несанкционированн"
                ],
                "обычные сигналы": [
                    "парол", "подозрительн", "вирус", "логин", "аккаунт",
                    "двухфактор", "учетнаязапись"
                ]
            }
        }
        self.priorityCategories = ["спам", "автоответчики/noreply сообщения"]
        self.whitelist = []
        whitelistPath = Path("../UserInfo/white_list.txt")
        lines = whitelistPath.read_text(encoding="utf-8").splitlines()
        for line in lines:
            if line.strip() != "":
                self.whitelist.append(line.strip())
        logging.info(f"Загружен белый список: {len(self.whitelist)} адресов")

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
        return 0

    def calculate_category_score(self, categoryName: str, subjectWords: list, bodyWords: list) -> int:
        score = 0
        for word in subjectWords:
            wordScore = self.calculate_word_score(word, categoryName)
            score += wordScore * 3
        for word in bodyWords:
            wordScore = self.calculate_word_score(word, categoryName)
            score += wordScore * 1
        logging.info(f"Категория '{categoryName}': итоговый балл = {score}")
        return score

    def classify(self, subject: str = "", body: str = "", sender: str = "") -> str:
        if sender in self.whitelist:
            logging.info("Адрес отправителя находится в белом списке, поэтому выбираем категорию 'важное'")
            return "важное"
        if "noreply" in sender or "no-reply" in sender:
            logging.info("Письмо отправителя не требует ответа, поэтому выбираем категорию 'автоответчики/noreply сообщения'")
            return "автоответчики/noreply сообщения"
        subjectWords = self.extract_words(subject)
        bodyWords = self.extract_words(body)
        for priorityCategory in self.priorityCategories:
            if priorityCategory in self.categories:
                score = self.calculate_category_score(priorityCategory,subjectWords, bodyWords)
                if score >= self.minscore:
                    logging.info(f"Выбираем категорию {priorityCategory} (балл: {score})")
                    return priorityCategory

        scores = {}
        for categoryName in self.categories:
            if categoryName in self.priorityCategories:
                continue
            score = self.calculate_category_score(categoryName, subjectWords, bodyWords)
            if score > 0:
                scores[categoryName] = score
        if not scores:
            logging.info("Нет совпадений, поэтому выбираем категорию 'прочее'")
            return "прочее"

        bestCategory = max(scores.keys(), key=lambda c: scores[c])
        bestScore = scores[bestCategory]
        if bestScore < self.minscore:
            logging.info(f"Выбираем категорию 'прочее' (максимальный балл {bestScore} ниже порога {self.minscore})")
            return "прочее"
        logging.info(f"Выбираем наиболее подходящую категорию {bestCategory} (балл: {bestScore})")
        return bestCategory

    def move_file_to_category(self, filePath: Path, categoryKey: str, name:str):
        targetFolder = self.pathCat.get(categoryKey, self.pathCat["прочее"])
        shutil.move(str(filePath), str(targetFolder))
        logging.info(f"Файл {name} отправлен в категорию {categoryKey}")