from pathlib import *

while True:
    print("Введите номер желаемого действия: ")
    print(" (1) Изменить путь для почтового ящика")
    print(" (2) Изменить адреса в белом списке")
    print(" (3) Завершить настройку")
    userChoise = input()
    if userChoise == "1":
        pathSettings = Path("../UserInfo/path_To_Inbox.txt")
        while (True):
            print("Введите путь до папки почтового ящика: ")
            filePath = Path(input())
            if not filePath.exists():
                print("Ошибка: путь не существует")
                print("Продолжить выбор? ")
                print(" (1) Да")
                print(" (2) Нет")
                userChoise2 = input()
                if userChoise2 == "0":
                    print("Настройка пути не была выполнена, путь не обновлён")
                    break
            elif not filePath.is_dir():
                print("Ошибка: это не папка")
                print("Продолжить выбор? ")
                print(" (1) Да")
                print(" (2) Нет")
                userChoise2 = input()
                if userChoise2 == "0":
                    print("Настройка пути не была выполнена, путь не обновлён")
                    break
            elif len(list(filePath.iterdir())) == 0:
                print("Папка пустая, продолжить? ")
                print(" (1) Да")
                print(" (2) Нет")
                userChoise2 = input()
                if userChoise2 == "1":
                    pathSettings.write_text(str(filePath), encoding="utf-8")
                    print("Путь сохранён")
                    break
            else:
                pathSettings.write_text(str(filePath), encoding="utf-8")
                print("Путь сохранён")
                break

    elif userChoise == "2":
        print("Введите путь до папки почтового ящика: ")
        filename = input()
    elif userChoise == "3":
        print("Завершение работы...")
        break
    else:
        print("Ошибка. Неверный формат ввода, пишите только цифру от 1 до 3")
