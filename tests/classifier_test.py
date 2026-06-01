from src.Classifier import *
import pytest


clf = Classifier()


def test_extract_words():
    result = clf.extract_words("не отчёт как что делать возможно ли учетная запись")
    assert result == ["неотчет", "какчтоделать", "возможноли", "учетнаязапись"]


def test_calculate_word_score2():
    key_signals = [
                    "инцидент", "сбой", "недоступ", "упал", "критич", "останов"
                    "авари", "краш", "срочно", "перегруз", "массов"
                ]
    for signal in key_signals:
        score = clf.calculate_word_score(signal, "инциденты")
        assert score == 2


def test_calculate_word_score1():
    default_signals = [
                    "останов", "неоткрыва", "неработа", "слома", "тормоз"
                    "незагружа", "неотвеча", "переустанов"
                ]
    for signal in default_signals:
        score = clf.calculate_word_score(signal, "инциденты")
        assert score == 1


def test_calculate_word_score0():
    default_signals = '1234 gfjkdk лпл ывдаыв щзпрщпиь13240 лаб43шщшот'.split()
    for signal in default_signals:
        score = clf.calculate_word_score(signal, "инциденты")
        assert score == 0


def test_calculate_category_score():
    subject = clf.extract_words("инцидент")
    body = clf.extract_words("")

    score = clf.calculate_category_score("инциденты", subject, body)
    assert score == 6


def test_classify1():
    result = clf.classify(subject="ваш заказ", body="спасибо", sender="noreply@shop.com")
    assert result == "автоответчики/noreply сообщения"


def test_classify2():
    result = clf.classify(subject="вы выиграли приз", body="", sender="promo@casino.com")
    assert result == "спам"


def test_classify3():
    def test_classify_incident_in_subject():
        result = clf.classify(subject="критический сбой базы данных", body="", sender="admin@company.com")
        assert result == "инциденты"


def test_classify4():
    def test_classify_question_request():
        result = clf.classify(subject="прошу выдать доступ к компьютеру", body="", sender="user@company.com")
        assert result == "вопросы/просьбы"


def test_classify5():
    result = clf.classify(subject="фишинг атака на аккаунт", body="", sender="security@company.com")
    assert result == "безопасность"


def test_classify6():
    result = clf.classify(subject="", body="", sender="unknown@x.com")
    assert result == "прочее"