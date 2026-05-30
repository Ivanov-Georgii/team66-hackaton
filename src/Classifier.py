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

    def extract_words(self, text: str) -> list:
        words = re.findall(r'[а-яa-z]{3,}', text.lower())
        return list(words)

    def calculate_word_score(self, word: str, categoryName: str) -> tuple:
        categoryData = self.categories.get(categoryName, {})
        for signal in categoryData.get("ключевые сигналы", []):
            if signal in word:
                return self.weights["ключевые сигналы"], "ключевые", signal

        for signal in categoryData.get("обычные сигналы", []):
            if signal in word:
                return self.weights["обычные сигналы"], "обычные", signal

        for signal in categoryData.get("антисигналы", []):
            if signal in word:
                return self.weights["антисигналы"], "анти", signal
        return 0, None, None

    def calculate_category_score(self, categoryName: str, subjectWords: list, bodyWords: list) -> tuple:
        matchedKey = []
        matchedRegular = []
        matchedAnti = []
        score = 0

        for word in subjectWords:
            wordScore, signalType, signal = self.calculate_word_score(word, categoryName)
            if wordScore > 0:
                score += wordScore * 2
                if signalType == "ключевые":
                    matchedKey.append(signal)
                elif signalType == "обычные":
                    matchedRegular.append(signal)
                elif signalType == "анти":
                    matchedAnti.append(signal)

        for word in bodyWords:
            wordScore, signalType, signal = self.calculate_word_score(word, categoryName)
            if wordScore > 0:
                score += wordScore * 1
                if signalType == "ключевые":
                    matchedKey.append(signal)
                elif signalType == "обычные":
                    matchedRegular.append(signal)
                elif signalType == "анти":
                    matchedAnti.append(signal)

        return score, matchedKey, matchedRegular, matchedAnti

    def classify(self, subject: str = "", body: str = "") -> tuple:
        subjectWords = self.extract_words(subject)
        bodyWords = self.extract_words(body)
        for priorityCategory in self.priorityCategories:
            if priorityCategory in self.categories:
                score, matchedKey, matchedRegular, matchedAnti = self.calculate_category_score(priorityCategory,subjectWords, bodyWords)
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
            score, matchedKey, matchedRegular, matchedAnti = self.calculate_category_score(categoryName, subjectWords, bodyWords)
            if score > 0:
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