from app.handlers import load_primary, load_secondary
from app.imports import describe


def test_primary():
    assert "widget" in load_primary('{"name":" Widget ","size":2,"tags":["a"]}')


def test_secondary():
    assert "widget" in load_secondary('{"name":" Widget ","size":2,"tags":["a"]}')


def test_describe():
    assert describe() == "localhost"
