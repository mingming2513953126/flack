# encoding: utf-8
'''
@author: lileilei
@file: models.py
@time: 2017/5/6 19:28
'''
from app import db
import datetime
from werkzeug.security import generate_password_hash,check_password_hash
class User(db.Model):#用户表
    __tablename__ ='user'
    uer_id=db.Column(db.Integer,primary_key=True,autoincrement=True)#用户id
    user_name=db.Column(db.String(64))#用户名
    password=db.Column(db.String(64))#用户密码
    status=db.Column(db.Integer)
    level=db.Column(db.Integer)
    user_zhuce_date=db.Column(db.DateTime,default=datetime.datetime.now())#注册时间
    user_zhuce_email=db.Column(db.String(64))#注册ip
    user_iphone=db.Column(db.Integer)#手机号
    user_qq=db.Column(db.Integer)#qq
    def __repr__(self):
        return '<User %r>' % self.user_name
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
class Model(db.Model):#模块
    __tablename__ ='model'
    model_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    model_name = db.Column(db.String(256))
    status = db.Column(db.Integer)
class Interface(db.Model):#接口
    __tablename__ ='Interface'
    interface_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    model_id=db.Column(db.Integer,db.ForeignKey('model.model_id'))#对应模块的名字
    interface_name=db.Column(db.String(64))#接口名字
    interface_url=db.Column(db.String(1024))#接口地址
    interface_methd=db.Column(db.String(64))#接口请求方式
    request_exam=db.Column(db.String(4096))#请求
    reposnese_exam=db.Column(db.String(4096))#返回
    stasus=db.Column(db.Integer)#状态
    def __repr__(self):
        return '<Interface name is :%r>'%self.interface_name
class Parameter(db.Model):
    __tablename__ ='Parameter'
    parameter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interface_id = db.Column(db.Integer, db.ForeignKey("interface.interface_id"))
    parameter_type = db.Column(db.String(64))
    parameter_group_id = db.Column(db.Integer)
    parameter_name = db.Column(db.String(64))
    necessary = db.Column(db.String(64))
    type = db.Column(db.String(64))
    default = db.Column(db.String(64))
    remark = db.Column(db.String(64))
    level = db.Column(db.String(64))
class Interface_ceshi(db.Model):
    __tablename__='Interface_ceshi'
    inter_ce_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    inter_ce_bianhao=db.Column(db.Integer)#接口编号
    inter_ce_url=db.Column(db.String(128))#接口地址
    inter_ce_meth=db.Column(db.String(64))#接口请求方法
    inter_ce_name=db.Column(db.String(64))
    inter_ce_zhushi = db.Column(db.String(64))
    inter_ce_assert = db.Column(db.String(1024))
    inter_ce_geshi=db.Column(db.String(64))
    inter_ce_data=db.Column(db.String(1024))


