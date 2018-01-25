# encoding: utf-8
'''
@author: lileilei
@file: db_create.py
@time: 2017/5/6 19:27
'''

from config import SQLALCHEMY_MIGRATE_REPO,SQLALCHEMY_DATABASE_URI
from app import db
import os
db.create_all()
