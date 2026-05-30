while True:
    print("Введите номер желаемого действия: ")
    print(" (1) Изменить путь для почтового ящика")
    print(" (2) Изменить адреса в белом списке")
    print(" (3) Завершить настройку")
    userChoise = input()
    if userChoise == "1":
        print("Введите путь до папки почтового ящика: ")
        filePath = input()
    elif userChoise == "2":
        print("Введите путь до папки почтового ящика: ")
        filename = input()
    elif userChoise == "3":
        print("Завершение работы...")
        break