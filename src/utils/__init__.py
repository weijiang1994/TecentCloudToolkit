"""
coding:utf-8
file: __init__.py.py
@time: 2024/6/17 23:17
@desc:
"""
import os

import yaml

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    def __init__(self):
        self.config = self.load_config()

    @staticmethod
    def load_config():
        with open(os.path.join(basedir, 'config/config.yml'), 'r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def get_config(self):
        return self.config


cfg = Config().get_config()
