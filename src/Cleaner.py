from pathlib import Path
import shutil

class Cleaner:
    def __init__(self):
        self.sortedInbox = Path("../SortedInbox")
        self.trash = Path("../Trash")

    def clean(self):
        for folder in self.sortedInbox.iterdir():
            for file in folder.iterdir():
                if not file.is_file():
                    continue
                if file.name == ".gitkeep":
                    continue
                shutil.move(str(file), "../Trash/" + file.name)
        print("Все файлы перемещены в корзину")

    def empty_trash(self):
        for file in self.trash.iterdir():
            if not file.is_file():
                continue
            file.unlink()
        print("Корзина очищена")

    def cleaner(self):
        while True:
            print("Введите номер желаемого действия: ")
            print(" (1) Переместить отсортированный ящик в корзину")
            print(" (2) Очистить корзину")
            print(" (3) Назад")
            userChoise = input()

            if userChoise == "1":
                self.clean()
            elif userChoise == "2":
                self.empty_trash()
            elif userChoise == "3":
                break
            else:
                print("Ошибка. Неверный формат ввода, пишите только цифру от 1 до 3")