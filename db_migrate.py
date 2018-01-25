# encoding: utf-8
'''
@author: lileilei
@file: db_migrate.py
@time: 2017/5/8 20:05
'''
from flask_migrate import Migrate,MigrateCommand
from flask_script import  Manager
from .app import db,app
manage=Manager(app)
migrate=Migrate(app,db)
manage.add_command('db',MigrateCommand)
if __name__=='__main__':
    manage.run()