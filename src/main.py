from FileReader import *
from Settings import *

settings = Settings()
settings.Settings()

data = FileReader("/Users/georgiy/Desktop/Хакатон/inbox")

print(data.read_files())