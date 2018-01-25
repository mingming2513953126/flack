# encoding: utf-8
'''
@author: lileilei
@file: forms.py
@time: 2017/5/6 19:28
'''
from flask_wtf import Form
from wtforms import StringField, TextField, PasswordField, FormField, SubmitField, FieldList, IntegerField
from wtforms.validators import Required, DataRequired
class LoginForm(Form):#登录表单
    username = StringField("登陆名", validators=[Required()])
    password = PasswordField("密码", validators=[Required()])
class ModelForm(Form):
    model_name = StringField("中文名称", validators=[Required()])
class InterfaceForm(Form): #接口表单
    interface_name = StringField("接口名称", validators=[Required()])
    interface_url = StringField("接口地址", validators=[Required()])
    interface_method = StringField("接口方法", validators=[Required()])
    request_exam = TextField("请求示例", validators=[Required()])
    response_exam = TextField("返回示例", validators=[Required()])#
class ParameterRequestForm(Form):
    parameter_group_id = StringField("从属", validators=[Required()])
    parameter_name = StringField("参数名称", validators=[Required()])
    necessary = StringField("是否必须", validators=[Required()])
    type = StringField("类型", validators=[Required()])
    default = StringField("默认值", validators=[Required()])
    remark = StringField("备注", validators=[Required()])
    level = StringField("层级", validators=[Required()])
class ParameterResponseForm(Form):
    parameter_group_id = StringField("从属", validators=[Required()])
    parameter_name = StringField("参数名称", validators=[Required()])
    necessary = StringField("是否必须", validators=[Required()])
    type = StringField("类型", validators=[Required()])
    default = StringField("示例", validators=[Required()])
    remark = StringField("描述", validators=[Required()])
    level = StringField("层级", validators=[Required()])
class SubmitForm(Form): #提交按钮
    submit = SubmitField("保存")
class ReguistForm(Form):#注册表单
    user_name=StringField('用户名',validators=[Required()])
    password=PasswordField('密码',validators=[Required()])
    que_password=PasswordField('密码',validators=[Required()])
    iphone=IntegerField('手机号',validators=[Required()])
    qq=IntegerField('qq号',validators=[Required()])
    email=StringField('邮箱',validators=[Required()])
class Ceshi(Form):
    Interface_bianhao=IntegerField('接口编号',validators=[Required()])
    Interface_url=StringField('接口地址',validators=[Required()])
    Interface_method=StringField('接口方法',validators=[Required()])
    Interface_name=StringField('接口名字',validators=[Required()])
    Interface_zhushi=StringField('接口注释',validators=[Required()])
    Interface_assert=StringField('接口断言',validators=[Required()])
    Interface_fanhui_geshi=StringField('接口返回格式',validators=[Required()])
    Interface_canshu=StringField('接口参数',validators=[Required()])
class email(Form):
    Interface_admin_email=StringField('管理邮件',validators=[Required()])
    Interface_admin_password=StringField('管理邮件密码',validators=[Required()])
    Interface_baogao_email=StringField('接受报告邮箱',validators=[Required()])