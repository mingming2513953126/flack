# -*- coding: utf-8 -*-
# @Date    : 2017-08-10 21:11:38
# @Author  : lileilei
from app import app
from .views import *
app.add_url_rule('/',view_func=IndexView.as_view('index'))
app.add_url_rule('/font',view_func=FontView.as_view('font'))
app.add_url_rule('/front_model/<int:model_id>',view_func=Font_modelView.as_view('front_model'))
app.add_url_rule('/home',view_func=HomeView.as_view('home'))
app.add_url_rule('/login',view_func=Login.as_view('login'))
app.add_url_rule('/eidituser/<string:user_name>',view_func=Eidituser.as_view('eidituser'))
app.add_url_rule('/delete/<user_name>',view_func=DeleteView.as_view('deleteusername'))
app.add_url_rule('/register',view_func=Register.as_view('register'))
app.add_url_rule('/users',view_func=UserView.as_view('users'))
app.add_url_rule('/editparameter_response/<model_id>&<interface_id>&<parameter_id>',view_func=Editparameter_reposseView.as_view('editparameter_response'))