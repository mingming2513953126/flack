# encoding: utf-8
'''
@author: lileilei
@file: config.py
@time: 2017/5/6 19:27
'''
import os
basedir=os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "api.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
CSRF_ENABLED = True
SECRET_KEY='leizi'  #hard
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = '25'
MAIL_USE_TLS = True
MAIL_USERNAME ='oyellow6@163.com'
MAIL_PASSWORD= 'qwer1234'
POSTS_PER_PAGE=6