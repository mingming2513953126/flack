# encoding: utf-8
'''
@author: lileilei
@file: manage.py
@time: 2017/5/6 19:27
'''
from app import app
import logging

if __name__=='__main__':
    handler = logging.FileHandler('.\log\\flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run()