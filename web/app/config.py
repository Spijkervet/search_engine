import json
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = 'config.json'
class Config():

    def __init__(self):
        handle = open(os.path.join(ROOT_DIR, CONFIG_FILE), 'r')
        self.config = json.loads(handle.read())
