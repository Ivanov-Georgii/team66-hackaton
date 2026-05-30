from pathlib import Path
import shutil

class FileReader:

    def __init__(self, folder):
        self.folder = Path(folder)
        self.unreadable = Path("../SortedInbox/Unreadable")
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
                bodyStart = -1
                count = 0
                body = ""
                for line in text.split("\n"):
                    if not line:
                        continue
                    else:
                        count+=1
                        if ((line.find("Subject:"))==0 or (line.find("Тема:"))==0) and iterSubject == False:
                            importantInfo[0]=(("Subject", line[line.find(":")+1:]))
                            firstIterSub = line
                            bodyStart = count
                            iterSubject = True
                        if ((line.find("From: "))==0 or (line.find("От кого: "))==0) and iterAdress == False:
                            importantInfo[1]=("From", line[line.find(":")+1:])
                            firstIterAdress = line
                            bodyStart = count
                            iterAdress = True
                for line in text.split("\n"):
                    if not line:
                        continue
                    else:
                        bodyStart -= 1
                        if bodyStart<0:
                            body+=line+" "
                importantInfo[2]=("Body",body)
                if not iterAdress:
                    shutil.move(str(file), str(self.unreadable / file.name))
                    print("отправляю файл "+file.name+" в битое")
                if body:
                    importantInfo[2]=("Body",body)
                data.append(importantInfo)
            except:
                print("Пропускаю:", file.name)
                try:
                    file.rename(self.unreadable / file.name)
                except:
                    pass
        return data
