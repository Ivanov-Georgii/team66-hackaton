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