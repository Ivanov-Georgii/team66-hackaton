import re

class Classifier:
    def __init__(self):
        self.weights = {"ключевые сигналы": 2, "обычные сигналы": 1, "антисигналы": -1}
        self.minscore = 3
        self.categories = {
            "инциденты": {
                "ключевые сигналы": ["ошибк", "баг", "сломал", "не работает", "упал", "сбой", "срочно"],
                "обычные сигналы": ["проблем", "завис", "не загружает", "не открывает", "недоступ", "падени"],
                "антисигналы": ["план", "обновлени", "релиз", "запланирован"]
            },
            "спам": {
                "ключевые сигналы": ["акци", "скидк", "бесплатно", "выиграл", "реклам"],
                "обычные сигналы": ["купить", "успей", "предложени", "распродаж", "инвестици", "заработ", "криптовалют",
                                    "биткоин"],
                "антисигналы": ["проект", "задач", "дедлайн", "отчёт", "работ", "коллег", "встреч", "бизнес", "клиент",
                                "договор", "счёт", "налог", "помоги", "вопрос", "ошибк", "баг"]
            },
            "вопросы/просьбы": {
                "ключевые сигналы": ["помоги", "подскажи", "нужна помощь", "просьб"],
                "обычные сигналы": ["как сделать", "не могу", "не можем", "вопрос", "помощь", "объясни", "что делать",
                                    "как быть", "возможно ли", "пожалуйста"],
                "антисигналы": ["срочно", "ошибк", "баг", "упал", "сломал"]
            },
            "автоответчики/noreply сообщения": {
                "ключевые сигналы": ["noreply", "autoreply", "автоответчик", "не отвечать"],
                "обычные сигналы": ["уведомлени", "нотификаци", "автоматическ", "сформирован", "создан", "сгенерирован",
                                    "notification", "отчет сформирован", "отчёт сформирован", "ваш заказ", "ваш платёж",
                                    "ваш отчёт", "доставлен", "отправлен", "получен"],
                "антисигналы": ["помоги", "срочно", "ответь", "пожалуйста ответь"]
            },
            "безопасность": {
                "ключевые сигналы": ["парол", "взлом", "утечк", "фишинг"],
                "обычные сигналы": ["безопасность", "подозрительн", "несанкционированн", "доступ", "учётная запись",
                                    "вирус", "вредоносн"],
                "антисигналы": ["проект", "задач", "помоги", "вопрос", "отчёт"]
            }
        }

        self.priorityCategories = ["спам", "автоответчики/noreply сообщения"]
        self.names = {category: category for category in self.categories}
        self.names["other"] = "прочее"

    def extract_words(self, text: str) -> set:
        words = re.findall(r'\b[а-яa-z]{3,}\b', text.lower())
        return set(words)

    def calculate_category_score(self, categoryName: str, words: set) -> tuple:
        categoryData = self.categories.get(categoryName, {})
        keySignals = set(categoryData.get("ключевые сигналы", []))
        regularSignals = set(categoryData.get("обычные сигналы", []))
        antiSignals = set(categoryData.get("антисигналы", []))
        matchedKey = []
        matchedRegular = []
        matchedAnti = []

        for word in words:
            for signal in keySignals:
                if signal in word:
                    matchedKey.append(signal)
                    break
            for signal in regularSignals:
                if signal in word:
                    matchedRegular.append(signal)
                    break
            for signal in antiSignals:
                if signal in word:
                    matchedAnti.append(signal)
                    break

        score = (len(matchedKey) * self.weights["ключевые сигналы"] +
                 len(matchedRegular) * self.weights["обычные сигналы"] +
                 len(matchedAnti) * self.weights["антисигналы"])

        return score, matchedKey, matchedRegular, matchedAnti

    def classify(self, subject: str = "", body: str = "") -> tuple:
        text = subject + " " + body
        words = self.extract_words(text)
        for priorityCategory in self.priorityCategories:
            if priorityCategory in self.categories:
                score, matchedKey, matchedRegular, matchedAnti = self.calculate_category_score(priorityCategory, words)
                if score >= self.minscore:
                    details = {
                        priorityCategory: {
                            "ключевые сигналы": matchedKey,
                            "обычные сигналы": matchedRegular,
                            "антисигналы": matchedAnti
                        }
                    }
                    return priorityCategory, {priorityCategory: score}, score, details

        scores = {}
        details = {}
        for categoryName in self.categories:
            if categoryName in self.priorityCategories:
                continue
            score, matchedKey, matchedRegular, matchedAnti = self.calculate_category_score(categoryName, words)
            if score != 0:
                scores[categoryName] = score
                details[categoryName] = {
                    "ключевые сигналы": matchedKey,
                    "обычные сигналы": matchedRegular,
                    "антисигналы": matchedAnti
                }
        if not scores:
            return "прочее", {}, 0, {}

        bestCategory = max(scores.keys(), key=lambda c: scores[c])
        bestScore = scores[bestCategory]
        if bestScore < self.minscore:
            return "прочее", scores, bestScore, details
        return bestCategory, scores, bestScore, details

    def get_category_name(self, categoryKey: str) -> str:
        return self.names.get(categoryKey, categoryKey)