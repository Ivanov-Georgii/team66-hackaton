from pathlib import Path
import shutil
import logging

class FileReader:

    def __init__(self, folder):
        self.folder = Path(folder)
        self.unreadable = Path("../SortedInbox/Unreadable")
        logging.info(f"FileReader готов к работе. Папка: {self.folder}")
    def read_files(self):
        data = []
        for file in self.folder.iterdir():
            if not file.is_file():
                continue
            try:
                text = file.read_text(encoding="utf-8")
                text = text.lower()
                iterSubject = False
                iterAdress = False
                importantInfo = [[],[],[],[]]
                bodyStart = -1
                count = 0
                body = ""
                for line in text.split("\n"):
                    if not line:
                        continue
                    else:
                        count+=1
                        if (line.find("subject:") == 0 or line.find("тема:") == 0 or line.find("tema:") == 0) and iterSubject == False:
                            importantInfo[0] = ("Subject", line[line.find(":") + 1:])
                            bodyStart = count
                            iterSubject = True
                        if (line.find("from:") == 0 or line.find("от кого:") == 0 or line.find("ot kogo:") == 0) and iterAdress == False:
                            if line.count("<") > 0:
                                importantInfo[1] = ("From", line[line.find("<") + 1: line.find(">")])
                            else:
                                importantInfo[1] = ("From", line[line.find(":") + 1:])
                            bodyStart = count
                            iterAdress = True
                if not iterSubject:
                    importantInfo[0] = ("Subject", "")
                    logging.info(f"В файле {file.name} не найдена тема")
                if not iterAdress:
                    importantInfo[1] = ("From", "")
                    logging.info(f"В файле {file.name} не найден отправитель")
                for line in text.split("\n"):
                    if not line:
                        continue
                    else:
                        bodyStart -= 1
                        if bodyStart<0:
                            body+=line+" "
                importantInfo[2] = ("Body",body)
                importantInfo[3] = ("Name",file.name)
                if not iterAdress:
                    shutil.move(str(file), str(self.unreadable / file.name))
                    logging.info(f"Файл {file.name} отправлен в категорию 'несортируемые'")
                    print("Файл " + file.name + " отправлен в несортируемые")
                    continue
                data.append(importantInfo)
            except:
                logging.error(f"Файл {file.name} не удалось прочитать, поэтому он отправлен в категорию 'несортируемые'")
                print("Файл " + file.name + " отправлен в несортируемые")
                try:
                    file.rename(self.unreadable / file.name)

                except:
                    pass
        return data
