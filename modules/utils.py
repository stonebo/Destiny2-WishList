import os
import hashlib


def workspace():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def gen_hash(text: str) -> str:
    return hashlib.sha1(text.encode("ascii")).hexdigest()
