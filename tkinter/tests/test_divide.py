from src import main

def test_divide_op():
    assert main.Divide.execute(None, 5, 0) == 'kan ikke dele på 0'

def test_divide_op1():
    assert main.Divide.execute(None, 4, 2) == 2

def test_divide_op2():
    assert main.Divide.execute(None, 8, 0) == 4