from FileReader import *
from Settings import *

settings = Settings()
settings.Settings()

pathFile = Path("../UserInfo/path_To_Inbox.txt")
if not pathFile.exists():
    print("Ошибка: файл с путём не найден, запустите настройку")
else:
    inboxPath = pathFile.read_text(encoding="utf-8").strip()
data = FileReader(inboxPath)

print(data.read_files())