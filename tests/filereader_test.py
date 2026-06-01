from src.FileReader import *
import pytest
from pathlib import Path

frd = FileReader('..\TestFolder')


def test1():
    frd.unreadable = Path("TestFolder/Unreadable")
    result = frd.read_files()
    assert result[0][0] == ("Subject", " test")
    assert result[0][1] == ("From", " test@mail.com")


def test2():
    frd.unreadable = Path("TestFolder/Unreadable")
    frd.read_files()
    moved_file = Path("TestFolder/Unreadable/mail2.txt")
    assert moved_file.exists() == False

def test3():
    frd.unreadable = Path("TestFolder/Unreadable")
    result = frd.read_files()
    found = False
    for item in result:
        if item[3][1] == "mail3.txt":
            assert "text message" in item[2][1]
            found = True
    assert found


def test4():
    frd.unreadable = Path("TestFolder/Unreadable")
    result = frd.read_files()
    found = False
    for item in result:
        if item[3][1] == "mail4.txt":
            assert item[1] == ("From", "user@mail.com")
            found = True
    assert found


def test5():
    frd.unreadable = Path("TestFolder/Unreadable")
    result = frd.read_files()
    found = False
    for item in result:
        if item[3][1] == "mail5.txt":
            assert item[0] == ("Subject", "")
            found = True
    assert found
