from src.testWork.main import inc  # content of test_sample.py


def test_answer():
    assert inc(3) == 3


def test_answer2():
    assert inc(8) == 9
