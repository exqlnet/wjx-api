# encoding=utf-8
from datetime import datetime


def log(*info):
    print(datetime.now(), *info)
