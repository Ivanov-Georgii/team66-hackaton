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


def test_kostil():
    src = Path("../SortedInbox/Unreadable/mail2.txt")
    dst = Path("../TestFolder/mail2.txt")
    if src.exists():
        src.replace(dst)