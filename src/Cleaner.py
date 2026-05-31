from pathlib import Path
import shutil
import logging

class Cleaner:
    def __init__(self):
        self.sortedInbox = Path("../SortedInbox")
        self.trash = Path("../Trash")

    def clean(self):
        logging.info("Начало перемещения файлов в корзину")
        for folder in self.sortedInbox.iterdir():
            for file in folder.iterdir():
                if not file.is_file():
                    continue
                if file.name == ".gitkeep":
                    continue
                shutil.move(str(file), "../Trash/" + file.name)
        logging.info("Все файлы перемещены в корзину")
        print("Все файлы перемещены в корзину")

    def empty_trash(self):
        logging.info("Начало очистки корзины")
        for file in self.trash.iterdir():
            if not file.is_file():
                continue
            if file.name == ".gitkeep":
                continue
            file.unlink()
        logging.info("Корзина очищена")
        print("Корзина очищена")

    def cleaner(self):
        logging.info("Открыто меню очистки")
        while True:
            print("Введите номер желаемого действия: ")
            print(" (1) Переместить отсортированный ящик в корзину")
            print(" (2) Очистить корзину")
            print(" (3) Назад")
            userChoise = input()

            if userChoise == "1":
                logging.info("Выбрано действие: переместить отсортированный ящик в корзину")
                self.clean()
            elif userChoise == "2":
                logging.info("Выбрано действие: очистить корзину")
                self.empty_trash()
            elif userChoise == "3":
                logging.info("Выбрано действие: назад")
                break
            else:
                logging.warning("Неверный формат ввода: нужно ввести цифру от 1 до 3")
                print("Ошибка. Неверный формат ввода, пишите только цифру от 1 до 3")