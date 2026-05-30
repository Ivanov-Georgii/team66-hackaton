from pathlib import *

class Settings:
    def __init__(self):
        self.whiteList = Path("../UserInfo/white_list.txt")
        self.pathSettings = Path("../UserInfo/path_To_Inbox.txt")
    def Settings(self):
        while True:
            print("Введите номер желаемого действия: ")
            print(" (1) Изменить путь для почтового ящика")
            print(" (2) Изменить адреса в белом списке")
            print(" (3) Завершить настройку")
            userChoise = input()

            if userChoise == "1":
                pathSettings = self.pathSettings
                while True:
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
                pathWhiteList = self.whiteList
                lines = pathWhiteList.read_text(encoding="utf-8").splitlines()
                emails = []
                for line in lines:
                    if line.strip() != "":
                        emails.append(line.strip())
                while True:
                    print("Введите номер желаемого действия: ")
                    print(" (1) Показать текущий список")
                    print(" (2) Добавить адрес")
                    print(" (3) Удалить адрес")
                    print(" (4) Назад")
                    userChoise2 = input()
                    if userChoise2 == "1":
                        if len(emails) == 0:
                            print("Белый список пуст")
                        else:
                            print("Текущий белый список:")
                            for i in range(len(emails)):
                                print(i+1, ") ", emails[i], sep="")
                    elif userChoise2 == "2":
                        print("Введите email-адрес для добавления: ")
                        newEmail = input().strip()
                        if "@" not in newEmail or "." not in newEmail:
                            print("Ошибка: некорректный формат email")
                        elif newEmail in emails:
                            print("Этот адрес уже есть в белом списке")
                        else:
                            emails.append(newEmail)
                            print("Адрес добавлен: " + newEmail)
                    elif userChoise2 == "3":
                        if len(emails) == 0:
                            print("Белый список пуст, нечего удалять")
                        else:
                            print("Текущий белый список:")
                            for i in range(len(emails)):
                                print("(", i+1, ") ", emails[i], sep="")
                            print("Введите номер адреса для удаления: ")
                            userChoise3 = input()
                            if userChoise3.isdigit() and 1 <= int(userChoise3) <= len(emails):
                                removedEmail = emails.pop(int(userChoise3)-1)
                                print("Адрес удалён: " + removedEmail)
                    elif userChoise2 == "4":
                        result = ""
                        for i in range(len(emails)):
                            if i < len(emails) - 1:
                                result = result + emails[i] + "\n"
                            else:
                                result = result + emails[i]
                        pathWhiteList.write_text(result, encoding="utf-8")
                        break

            elif userChoise == "3":
                print("Завершение работы...")
                break
            else:
                print("Ошибка. Неверный формат ввода, пишите только цифру от 1 до 3")
