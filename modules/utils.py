import os


def workspace():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))