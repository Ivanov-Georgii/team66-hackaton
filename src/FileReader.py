from pathlib import Path

class FileReader:

    def __init__(self, folder):
        self.folder = Path(folder)

    def read_files(self):
        for file in self.folder.iterdir():
            if not file.is_file():
                continue
            try:
                text = file.read_text()
                firstIterSub = ""
                firstIterAdress = ""
                iterSubject = False
                iterAdress = False
                importantInfo = []
                for line in text.split("\n"):
                    if not line:
                        continue
                    else:
                        if ((line.find("Subject: "))==0 or (line.find("Тема: "))==0) and iterSubject == False:
                            importantInfo.append(("Subject", line[line.find(":")+1:]))
                            firstIterSub = line
                            iterSubject = True
                        if ((line.find("From: "))==0 or (line.find("От кого: "))==0) and iterSubject == False:
                            importantInfo.append(("From", line[line.find(":")+1:]))
                            firstIterAdress = line
                            iterAdress = True
                        if iterSubject and iterAdress:
                            print(importantInfo)
                            break
                else:
                    print("отправить файл в битое")
                print("")
            except:
                print("Пропускаю:", file.name)

