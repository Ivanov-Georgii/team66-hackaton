from src.FileReader import *
from pathlib import Path
import shutil


def test1():
    frd = FileReader('../TestFolder')
    frd.unreadable = Path("../SortedInbox/Unreadable")
    result = frd.read_files()
    found = False
    for item in result:
        if item[3][1] == "mail1.txt":
            assert item[0] == ("Subject", "test")
            assert item[1] == ("From", "test@mail.com")
            found = True
    assert found


def test2():
    frd = FileReader('../TestFolder')
    frd.unreadable = Path("../SortedInbox/Unreadable")
    frd.read_files()
    moved_file = Path("TestFolder/Unreadable/mail2.txt")
    assert moved_file.exists() == False


def test3():
    frd = FileReader('../TestFolder')
    frd.unreadable = Path("../SortedInbox/Unreadable")
    result = frd.read_files()
    found = False
    for item in result:
        if item[3][1] == "mail3.txt":
            assert "text message" in item[2][1]
            found = True
    assert found


def test4():
    frd = FileReader('../TestFolder')
    frd.unreadable = Path("../SortedInbox/Unreadable")
    result = frd.read_files()
    found = False
    for item in result:
        if item[3][1] == "mail4.txt":
            assert item[1] == ("From", "user@mail.com")
            found = True
    assert found


def test5():
    frd = FileReader('../TestFolder')
    frd.unreadable = Path("../SortedInbox/Unreadable")
    result = frd.read_files()
    found = False
    for item in result:
        if item[3][1] == "mail5.txt":
            assert item[0] == ("Subject", "")
            found = True
    assert found


def test6():
    frd = FileReader('../TestFolder')
    frd.unreadable = Path("../SortedInbox/Unreadable")
    frd.read_files()
    moved_file = Path("../SortedInbox/Unreadable/mail6.txt")
    assert moved_file.exists()

def test7():
    frd = FileReader('../TestFolder')
    frd.unreadable = Path("../SortedInbox/Unreadable")
    frd.read_files()
    moved_file = Path("../SortedInbox/Unreadable/mail7.bin")
    assert moved_file.exists()


def test8():
    frd = FileReader('../TestFolder')
    frd.unreadable = Path("../SortedInbox/Unreadable")
    result = frd.read_files()
    found = False
    for item in result:
        if item[3][1] == "mail8.txt":
            assert item[1] == ("From", "a.fedorova@company.ru")
            assert item[0] == ("Subject", "izmenenie grafika raboty")
            found = True
    assert found


def test_kostil():
    shutil.move("../SortedInbox/Unreadable/mail2.txt", "../TestFolder/mail2.txt")
    shutil.move("../SortedInbox/Unreadable/mail6.txt", "../TestFolder/mail6.txt")
    shutil.move("../SortedInbox/Unreadable/mail7.bin", "../TestFolder/mail7.bin")