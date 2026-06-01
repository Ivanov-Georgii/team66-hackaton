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