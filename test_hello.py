# test_hello.py
from hello import greet

def test_greet_default():
    assert greet() == "Hello, World!"

def test_greet_name():
    assert greet("Vinayak") == "Hello, Vinayak!"
