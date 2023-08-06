import datetime
import os
import re


def create_model_directory(path: str):
    path = os.path.abspath(path)
    date_str = re.sub(':', '', datetime.datetime.now().replace(microsecond=0).isoformat())
    path = os.path.join(path, date_str)
    os.mkdir(path)

    return path
