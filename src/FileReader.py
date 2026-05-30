from pathlib import Path

class FileReader:

    def __init__(self, folder):
        self.folder = Path(folder)

    def read_files(self):
        data = []
        for file in self.folder.iterdir():
            if not file.is_file():
                continue
            try:
                text = file.read_text()
                firstIterSub = ""
                firstIterAdress = ""
                iterSubject = False
                iterAdress = False
                importantInfo = [[],[],[]]
                body = ""
                for line in text.split("\n"):
                    if not line:
                        continue
                    else:
                        if iterSubject and iterAdress:
                            body += line
                        if ((line.find("Subject: "))==0 or (line.find("Тема: "))==0) and iterSubject == False:
                            importantInfo[0]=(("Subject", line[line.find(":")+1:]))
                            firstIterSub = line
                            iterSubject = True
                        if ((line.find("From: "))==0 or (line.find("От кого: "))==0) and iterAdress == False:
                            importantInfo[1]=("From", line[line.find(":")+1:])
                            firstIterAdress = line
                            iterAdress = True
                if not iterAdress:
                    print("отправить файл в битое")
                if body:
                    importantInfo[2]=("Body",body)
                data.append(importantInfo)
            except:
                print("Пропускаю:", file.name)
        return data
