from FileReader import *
from Settings import *
from Classifier import *
from Cleaner import *
from pathlib import *
import logging

logging.basicConfig(filename="../Logs/run.log", encoding="utf-8", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

print("Здравствуйте, программа запущена")
logging.info("Программа запущена")
while True:
    print("Введите номер желаемого действия: ")
    print(" (1) Запустить сортировку ящика")
    print(" (2) Открыть настройки")
    print(" (3) Очистить отсортированный ящик")
    print(" (4) Завершить работу")
    userChoise = input()

    if userChoise == "1":
        logging.info("Пользователь выбрал (1) Запустить сортировку ящика")
        pathFile = Path("../UserInfo/path_To_Inbox.txt")
        if not pathFile.exists():
            print("Ошибка: файл с путём не найден, запустите настройку")
            logging.error("Ошибка: файл с путём не найден, запустите настройку")
        else:
            inboxPath = pathFile.read_text(encoding="utf-8").strip()
            if not inboxPath:
                print("Ошибка: путь не настроен, запустите настройку")
                logging.error("Ошибка: путь не настроен, запустите настройку")
            else:
                logging.info("Сортировка запущена, путь до сортируемой папки: " + str(inboxPath))
                data = FileReader(inboxPath).read_files()
                classifier = Classifier()
                for email in data:
                    filePath = Path(inboxPath) / email[3][1]
                    category = classifier.classify(email[0][1], email[2][1], email[1][1])
                    classifier.move_file_to_category(filePath, category, email[3][1])
                print("Сортировка завершена")
                logging.info("Сортировка завершена")

    elif userChoise == "2":
        logging.info("Пользователь выбрал (2) Открыть настройки")
        settings = Settings()
        settings.Settings()

    elif userChoise == "3":
        logging.info("Пользователь выбрал (3) Очистить отсортированный ящик")
        cleaner = Cleaner()
        cleaner.cleaner()

    elif userChoise == "4":
        logging.info("Пользователь выбрал (4) Завершить работу")
        break

    else:
        print("Ошибка. Неверный формат ввода, введите только цифру от 1 до 4")
        logging.error("Ошибка. Неверный формат ввода, введите только цифру от 1 до 4")