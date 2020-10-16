import json
from collections import namedtuple

def load(file):
    try:
        with open(file, encoding='utf8') as data:
            return json.load(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[33m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'