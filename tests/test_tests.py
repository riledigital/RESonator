# Basic test to see if our env even runs :o
# content of test_sample.py
def inc(x):
    return x + 1


# def test_answer_wrong():
#     assert inc(3) == 5


def test_answer():
    assert inc(3) == 4
