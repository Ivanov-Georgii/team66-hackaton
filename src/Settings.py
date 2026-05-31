from pathlib import *
import logging

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
                logging.info("Пользователь выбрал '(1) Изменить путь для почтового ящика'")
                pathSettings = self.pathSettings
                while True:
                    print("Введите путь до папки почтового ящика: ")
                    filePath = Path(input())
                    if not filePath.exists():
                        print("Ошибка: путь не существует")
                        logging.error("Ошибка: путь не существует")
                        print("Продолжить выбор? ")
                        print(" (1) Да")
                        print(" (2) Нет")
                        userChoise2 = input()
                        if userChoise2 == "2":
                            logging.info("Пользователь выбрал '(2) Не продолжать выбор пути'")
                            print("Настройка пути не была выполнена, путь не обновлён")
                            logging.warning("Настройка пути не была выполнена, путь не обновлён")
                            break
                        logging.info("Пользователь выбрал '(1) Продолжить выбор пути'")
                    elif not filePath.is_dir():
                        print("Ошибка: это не папка")
                        logging.error("Ошибка: это не папка")
                        print("Продолжить выбор? ")
                        print(" (1) Да")
                        print(" (2) Нет")
                        userChoise2 = input()
                        if userChoise2 == "2":
                            logging.info("Пользователь выбрал '(2) Не продолжать выбор пути'")
                            print("Настройка пути не была выполнена, путь не обновлён")
                            logging.warning("Настройка пути не была выполнена, путь не обновлён")
                            break
                        logging.info("Пользователь выбрал '(1) Продолжить выбор пути'")
                    elif len(list(filePath.iterdir())) == 0:
                        print("Папка пустая, продолжить? ")
                        logging.warning("Папка с ящиком писем пустая")
                        print(" (1) Да")
                        print(" (2) Нет")
                        userChoise2 = input()
                        if userChoise2 == "1":
                            logging.info("Пользователь выбрал '(1) Продолжить выбор пути'")
                            pathSettings.write_text(str(filePath), encoding="utf-8")
                            print("Путь сохранён")
                            logging.info("Пользователь выбрал путь до ящика: " + str(filePath))
                            break
                        logging.info("Пользователь выбрал '(2) Не продолжать выбор пути'")
                    else:
                        pathSettings.write_text(str(filePath), encoding="utf-8")
                        print("Путь сохранён")
                        logging.info("Пользователь выбрал путь до ящика: " + str(filePath))
                        break

            elif userChoise == "2":
                logging.info("Пользователь выбрал '(2) Изменить адреса в белом списке'")
                pathWhiteList = self.whiteList
                lines = pathWhiteList.read_text(encoding="utf-8").splitlines()
                emails = []
                for line in lines:
                    if line.strip() != "":
                        emails.append(line.strip())
                logging.info("Текущий белый список: ", *emails)
                while True:
                    print("Введите номер желаемого действия: ")
                    print(" (1) Показать текущий список")
                    print(" (2) Добавить адрес")
                    print(" (3) Удалить адрес")
                    print(" (4) Назад")
                    userChoise2 = input()
                    if userChoise2 == "1":
                        logging.info("Пользователь выбрал '(1) Показать текущий список'")
                        if len(emails) == 0:
                            print("Белый список пуст")
                            logging.info("Текущий белый лист пустой")
                        else:
                            print("Текущий белый список:")
                            for i in range(len(emails)):
                                print(i+1, ") ", emails[i], sep="")
                            logging.info("Текущий белый список: ", *emails)
                    elif userChoise2 == "2":
                        logging.info("Пользователь выбрал '(2) Добавить адрес'")
                        print("Введите email-адрес для добавления: ")
                        newEmail = input().strip().lower()
                        logging.info("Пользователь вввёл адрес ", newEmail)
                        if "@" not in newEmail or "." not in newEmail:
                            print("Ошибка: некорректный формат email")
                            logging.error("Ошибка: некорректный формат email")
                        elif newEmail in emails:
                            print("Этот адрес уже есть в белом списке")
                            logging.warning("Этот адрес уже есть в белом списке")
                        else:
                            emails.append(newEmail)
                            print("Адрес добавлен: " + newEmail)
                            logging.info("Адрес добавлен, белый список: " + ", ".join(emails))
                    elif userChoise2 == "3":
                        logging.info("Пользователь выбрал '(3) Удалить адрес'")
                        if len(emails) == 0:
                            print("Белый список пуст, нечего удалять")
                            logging.info("Белый список пуст, нечего удалять")
                        else:
                            print("Текущий белый список:")
                            for i in range(len(emails)):
                                print("(", i+1, ") ", emails[i], sep="")
                            print("Введите номер адреса для удаления: ")
                            userChoise3 = input()
                            logging.info("Пользователь вввёл адрес ", userChoise3)
                            if userChoise3.isdigit() and 1 <= int(userChoise3) <= len(emails):
                                removedEmail = emails.pop(int(userChoise3)-1)
                                print("Адрес удалён: " + removedEmail)
                                logging.info("Адрес удалён, белый список: " + ", ".join(emails))
                    elif userChoise2 == "4":
                        logging.info("Пользователь выбрал '(4) Назад'")
                        result = ""
                        for i in range(len(emails)):
                            if i < len(emails) - 1:
                                result = result + emails[i] + "\n"
                            else:
                                result = result + emails[i]
                        pathWhiteList.write_text(result, encoding="utf-8")
                        logging.info("Итоговый белый список: " + ", ".join(emails))
                        break

            elif userChoise == "3":
                logging.info("Пользователь выбрал '(3) Завершить настройку'")
                print("Завершение настройки")
                logging.info("Насторйка завершена")
                break
            else:
                print("Ошибка. Неверный формат ввода, введите только цифру от 1 до 3")
                logging.error("Ошибка. Неверный формат ввода, введите только цифру от 1 до 3")
