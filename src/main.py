from FileReader import *
from Settings import *
from Classifier import *

settings = Settings()
settings.Settings()

pathFile = Path("../UserInfo/path_To_Inbox.txt")
if not pathFile.exists():
    print("Ошибка: файл с путём не найден, запустите настройку")
else:
    inboxPath = pathFile.read_text(encoding="utf-8").strip()
    data = FileReader(inboxPath).read_files()
    classifier = Classifier()
    for email in data:
        filePath = Path(inboxPath) / email[3][1]
        category = classifier.classify(email[0][1], email[2][1], email[1][1])
        classifier.move_file_to_category(filePath, category)