# encoding: utf-8
'''
@author: lileilei
@file: views.py
@time: 2017/5/6 19:28
'''
from flask import render_template, redirect, session, url_for,flash,request
from flask_login import login_required
from app import db,mail,app
from .models import Interface, Model, User, Parameter
from .forms import LoginForm, ReguistForm,ModelForm, InterfaceForm, ParameterRequestForm, ParameterResponseForm, SubmitForm,Ceshi,email
import datetime
from flask_mail import  Mail,Message
from  flask import  g
from config import POSTS_PER_PAGE
from flask.views import MethodView,View
# 前台首页
class IndexView(View):
  methods=["GET", "POST"]
  def dispath_request(self):
      return render_template("index.html")
# 前台模块列表
class FontView(View):
  methods=["GET", "POST"]
  def dispath_request(self):
      model_all = Model.query.all()
      model_forms = []
      for i in range(len(model_all)):
          model_form = {"model_id": model_all[i].model_id,
                        "model_name": model_all[i].model_name}
          model_forms.append(model_form)
      return render_template("front.html",
                             model_forms=model_forms)
# 前台接口列表
class Font_modelView(View):
  methods=["GET", "POST"]
  def dispath_request(self,model_id):
      model_one = Model.query.filter_by(model_id=model_id).first()
      interface_model_all = Interface.query.filter_by(model_id=model_id).all()
      interface_model_forms = []
      for i in range(len(interface_model_all)):
          interface_model_form = {"interface_id": interface_model_all[i].interface_id,
                                  "interface_name": interface_model_all[i].interface_name,
                                  "interface_url": interface_model_all[i].interface_url}
          interface_model_forms.append(interface_model_form)
      return render_template("front_model.html",
                             model_id=model_id,
                             model_one=model_one,
                             interface_model_forms=interface_model_forms)
g_parameter_request = []
g_parameter_response = []
# 前台接口详情
@app.route("/front_interface/<model_id>&<interface_id>", methods=["GET", "POST"])
def front_interface(model_id, interface_id):
    global g_parameter_request, g_parameter_response
    model_one = Model.query.filter_by(model_id=model_id).first()
    interface_model_all = Interface.query.filter_by(model_id=model_id).all()
    interface_model_one = Interface.query.filter_by(interface_id=interface_id).first()
    interface_model_forms = []
    for i in range(len(interface_model_all)):
        interface_model_form = {"interface_id": interface_model_all[i].interface_id,
                                "interface_name": interface_model_all[i].interface_name,
                                "interface_url": interface_model_all[i].interface_url}
        interface_model_forms.append(interface_model_form)
    parameter_request_all = Parameter.query.filter_by(interface_id=interface_id, parameter_type=10).all()
    parameter_request_forms = []
    for i in range(len(parameter_request_all)):
        parameter_request_form = {"parameter_id": parameter_request_all[i].parameter_id,
                                  "parameter_name": parameter_request_all[i].parameter_name,
                                  "necessary": parameter_request_all[i].necessary,
                                  "type": parameter_request_all[i].type,
                                  "default": parameter_request_all[i].default,
                                  "remark": parameter_request_all[i].remark,
                                  "parameter_group_id": parameter_request_all[i].parameter_group_id,
                                  "level": parameter_request_all[i].level}
        parameter_request_forms.append(parameter_request_form)
    parameter_response_all = Parameter.query.filter_by(interface_id=interface_id, parameter_type=20).all()
    parameter_response_forms = []
    for i in range(len(parameter_response_all)):
        parameter_response_form = {"parameter_id": parameter_response_all[i].parameter_id,
                                   "parameter_name": parameter_response_all[i].parameter_name,
                                   "necessary": parameter_response_all[i].necessary,
                                   "type": parameter_response_all[i].type,
                                   "default": parameter_response_all[i].default,
                                   "remark": parameter_response_all[i].remark,
                                   "parameter_group_id": parameter_response_all[i].parameter_group_id,
                                   "level": parameter_response_all[i].level}
        parameter_response_forms.append(parameter_response_form)
    g_parameter_request = []    # 全局变量、清空列表数据
    g_parameter_response = []   # 全局变量、清空列表数据
    n_parameter_request(parameter_request_forms, parameter_request_all[0].parameter_group_id)
    n_parameter_response(parameter_response_forms,parameter_response_all[0].parameter_group_id)
    return render_template("front_interface.html",
                           model_id=model_id,
                           model_one=model_one,
                           interface_model_forms=interface_model_forms,
                           interface_model_one=interface_model_one,
                           g_parameter_request=g_parameter_request,
                           g_parameter_response=g_parameter_response)
# 请求参数排序
def n_parameter_request(request, parameter_group_id):
    for form in request:
        if form["parameter_group_id"] == parameter_group_id:
            new_parameter_group_id = form["parameter_id"]
            g_parameter_request.append(form)
            n_parameter_request(request, new_parameter_group_id)  
    return g_parameter_request
# 返回参数排序
def n_parameter_response(response, parameter_group_id):
    for form in response:
        if form["parameter_group_id"] == parameter_group_id:
            new_parameter_group_id = form["parameter_id"]
            g_parameter_response.append(form)
            n_parameter_response(response, new_parameter_group_id) 
    return g_parameter_response
# 后台首页
class HomeView(View):
  methods=["GET", "POST"]
  def dispath_request(self):
      if not session.get("logged_in"):
          return redirect(url_for("login"))
      return render_template("home.html")
# 后台登录
class Login(View):
  methods=["GET", "POST"]
  def dispath_request(self):
      form = LoginForm()
      if form.validate_on_submit():
          try:
              user_one = User.query.filter_by(user_name=form.username.data).first()
              me=user_one.check_password(form.password.data)
              if me==True  and user_one.status == 1:
                  session["logged_in"] = True
                  return redirect(url_for("home"))
              else:
                  flash('登录密码错误！请检测你的密码')
                  return render_template("login.html", form=form)
          except AttributeError:
              flash('登录fail！')
              return render_template("login.html", form=form)
      return render_template("login.html",
                             form=form)
# 后台登出
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("index"))
# 模块管理
@app.route("/model", methods=["GET", "POST"])
def model():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    model_all = Model.query.all()
    allhost = Model.query.paginate(2, POSTS_PER_PAGE, False).items
    model_forms = []
    for i in range(len(model_all)):
        model_form = {"model_id": model_all[i].model_id,
                      "model_name": model_all[i].model_name}
        model_forms.append(model_form)
    return render_template("model.html",
                           model_forms=model_forms,posts=allhost)
# 新增模块
@app.route("/addmodel", methods=["GET", "POST"])
def addmodel():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    add_model = ModelForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        add = Model(model_name=add_model.model_name.data)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("model"))
    return render_template("addmodel.html",
                           add_model=add_model,
                           submit=submit)
# 编辑模块
@app.route("/editmodel/<model_id>", methods=["GET", "POST"])
def editmodel(model_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    model_one = Model.query.filter_by(model_id=model_id).first()
    edit_model = ModelForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        model_one.model_name = edit_model.model_name.data
        db.session.commit()
        return redirect(url_for("model"))
    edit_model.model_name.data = model_one.model_name
    return render_template("editmodel.html",
                           edit_model=edit_model,
                           submit=submit)
# 接口列表
@app.route("/interface/<model_id>")
def interface(model_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    interface_model_all = Interface.query.filter_by(model_id=model_id).all()
    interface_model_forms = []
    for i in range(len(interface_model_all)):
        interface_model_form = {"interface_id": interface_model_all[i].interface_id,
                                "interface_name": interface_model_all[i].interface_name,
                                "interface_url": interface_model_all[i].interface_url}
        interface_model_forms.append(interface_model_form)
    return render_template("interface.html",
                           model_id=model_id,
                           interface_model_forms=interface_model_forms)
# 新增接口
@app.route("/addinterface/<model_id>", methods=["GET", "POST"])
def addinterface(model_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    add_interface = InterfaceForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        add = Interface(interface_name=add_interface.interface_name.data,
                        model_id=model_id,
                        interface_url=add_interface.interface_url.data,
                        interface_methd=add_interface.interface_method.data,
                        request_exam=add_interface.request_exam.data,
                        reposnese_exam=add_interface.response_exam.data)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("interface",
                                model_id=model_id))
    return render_template("addinterface.html",
                           add_interface=add_interface,
                           model_id=model_id,
                           submit=submit)
# 编辑接口
@app.route("/editinterface/<model_id>&<interface_id>", methods=["GET", "POST"])
def editinterface(model_id, interface_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    interface_model_one = Interface.query.filter_by(interface_id=interface_id).first()
    edit_interface_model = InterfaceForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        interface_model_one.interface_name = edit_interface_model.interface_name.data
        interface_model_one.interface_url = edit_interface_model.interface_url.data
        interface_model_one.interface_methd = edit_interface_model.interface_method.data
        interface_model_one.request_exam = edit_interface_model.request_exam.data
        interface_model_one.response_exam = edit_interface_model.response_exam.data
        db.session.commit()
        return redirect(url_for("interface",
                                model_id=model_id))
    edit_interface_model.interface_name.data = interface_model_one.interface_name
    edit_interface_model.interface_url.data = interface_model_one.interface_url
    edit_interface_model.interface_method.data = interface_model_one.interface_methd
    edit_interface_model.request_exam.data = interface_model_one.request_exam
    edit_interface_model.response_exam.data = interface_model_one.reposnese_exam
    return render_template("editinterface.html",
                           model_id=model_id,
                           interface_id=interface_id,
                           edit_interface_model=edit_interface_model,
                           submit=submit)
# 请求参数列表
@app.route("/parameter_request/<model_id>&<interface_id>", methods=["GET", "POST"])
def parameter_request(model_id, interface_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    parameter_request_all = Parameter.query.filter_by(interface_id=interface_id, parameter_type=10).all()
    parameter_request_forms = []
    for i in range(len(parameter_request_all)):
        parameter_request_form = {"parameter_id": parameter_request_all[i].parameter_id,
                                  "parameter_name": parameter_request_all[i].parameter_name,
                                  "necessary": parameter_request_all[i].necessary,
                                  "type": parameter_request_all[i].type,
                                  "default": parameter_request_all[i].default,
                                  "remark": parameter_request_all[i].remark,
                                  "parameter_group_id": parameter_request_all[i].parameter_group_id,
                                  "level": parameter_request_all[i].level}
        parameter_request_forms.append(parameter_request_form)
    return render_template("parameter_request.html",
                           model_id=model_id,
                           interface_id=interface_id,
                           parameter_request_forms=parameter_request_forms)
# 新增请求参数
@app.route("/addparameter_request/<model_id>&<interface_id>", methods=["GET", "POST"])
def addparameter_request(model_id, interface_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    add_parameter_request = ParameterRequestForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        add = Parameter(interface_id=interface_id,
                        parameter_type=10,
                        parameter_group_id=add_parameter_request.parameter_group_id.data,
                        parameter_name=add_parameter_request.parameter_name.data,
                        necessary=add_parameter_request.necessary.data,
                        type=add_parameter_request.type.data,
                        default=add_parameter_request.default.data,
                        remark=add_parameter_request.remark.data,
                        level=add_parameter_request.level.data)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("parameter_request",
                                model_id=model_id,
                                interface_id=interface_id))
    return render_template("addparameter_request.html",
                           add_parameter_request=add_parameter_request,
                           model_id=model_id,
                           interface_id=interface_id,
                           submit=submit)
# 编辑请求参数
@app.route("/editparameter_request/<model_id>&<interface_id>&<parameter_id>", methods=["GET", "POST"])
def editparameter_request(model_id, interface_id, parameter_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    parameter_request_one = Parameter.query.filter_by(parameter_id=parameter_id).first()
    edit_parameter_request = ParameterRequestForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        parameter_request_one.parameter_name = edit_parameter_request.parameter_name.data
        parameter_request_one.necessary = edit_parameter_request.necessary.data
        parameter_request_one.type = edit_parameter_request.type.data
        parameter_request_one.default = edit_parameter_request.default.data
        parameter_request_one.remark = edit_parameter_request.remark.data
        parameter_request_one.parameter_group_id = edit_parameter_request.parameter_group_id.data
        parameter_request_one.level = edit_parameter_request.level.data
        db.session.commit()
        return redirect(url_for("parameter_request",
                                model_id=model_id,
                                interface_id=interface_id))
    edit_parameter_request.parameter_name.data = parameter_request_one.parameter_name
    edit_parameter_request.necessary.data = parameter_request_one.necessary
    edit_parameter_request.type.data = parameter_request_one.type
    edit_parameter_request.default.data = parameter_request_one.default
    edit_parameter_request.remark.data = parameter_request_one.remark
    edit_parameter_request.parameter_group_id.data = parameter_request_one.parameter_group_id
    edit_parameter_request.level.data = parameter_request_one.level
    return render_template("editparameter_request.html",
                           model_id=model_id,
                           interface_id=interface_id,
                           parameter_id=parameter_id,
                           edit_parameter_request=edit_parameter_request,
                           submit=submit)
# 删除请求参数
@app.route("/deleteparameter_request/<model_id>&<interface_id>&<parameter_id>", methods=["GET", "POST"])
def deleteparameter_request(model_id, interface_id, parameter_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    deleteparameter_request_one = Parameter.query.filter_by(parameter_id=parameter_id).first()
    db.session.delete(deleteparameter_request_one)
    db.session.commit()
    parameter_request_all = Parameter.query.filter_by(interface_id=interface_id, parameter_type=10).all()
    parameter_request_forms = []
    for i in range(len(parameter_request_all)):
        parameter_request_form = {"parameter_id": parameter_request_all[i].parameter_id,
                                  "parameter_name": parameter_request_all[i].parameter_name,
                                  "necessary": parameter_request_all[i].necessary,
                                  "type": parameter_request_all[i].type,
                                  "default": parameter_request_all[i].default,
                                  "remark": parameter_request_all[i].remark,
                                  "parameter_group_id": parameter_request_all[i].parameter_group_id,
                                  "level": parameter_request_all[i].level}
        parameter_request_forms.append(parameter_request_form)
    return render_template("parameter_request.html",
                           model_id=model_id,
                           interface_id=interface_id,
                           parameter_request_forms=parameter_request_forms)
# 返回参数列表
@app.route("/parameter_response/<model_id>&<interface_id>", methods=["GET", "POST"])
def parameter_response(model_id, interface_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    parameter_response_all = Parameter.query.filter_by(interface_id=interface_id, parameter_type=20).all()
    parameter_response_forms = []
    for i in range(len(parameter_response_all)):
        parameter_response_form = {"parameter_id": parameter_response_all[i].parameter_id,
                                   "parameter_name": parameter_response_all[i].parameter_name,
                                   "necessary": parameter_response_all[i].necessary,
                                   "type": parameter_response_all[i].type,
                                   "default": parameter_response_all[i].default,
                                   "remark": parameter_response_all[i].remark,
                                   "parameter_group_id": parameter_response_all[i].parameter_group_id,
                                   "level": parameter_response_all[i].level}
        parameter_response_forms.append(parameter_response_form)
    return render_template("parameter_response.html",
                           model_id=model_id,
                           interface_id=interface_id,
                           parameter_response_forms=parameter_response_forms)
# 新增返回参数
@app.route("/addparameter_response/<model_id>&<interface_id>", methods=["GET", "POST"])
def addparameter_response(model_id, interface_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    add_parameter_response = ParameterResponseForm()
    submit = SubmitForm()
    if submit.validate_on_submit():
        add = Parameter(interface_id=interface_id,
                        parameter_type=20,
                        parameter_group_id=add_parameter_response.parameter_group_id.data,
                        parameter_name=add_parameter_response.parameter_name.data,
                        necessary=add_parameter_response.necessary.data,
                        type=add_parameter_response.type.data,
                        default=add_parameter_response.default.data,
                        remark=add_parameter_response.remark.data,
                        level=add_parameter_response.level.data)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("parameter_response",
                                model_id=model_id,
                                interface_id=interface_id))
    return render_template("addparameter_response.html",
                           add_parameter_response=add_parameter_response,
                           model_id=model_id,
                           interface_id=interface_id,
                           submit=submit)
# 编辑返回参数
class Editparameter_reposseView(View): 
  methods=["GET", "POST"]
  def dispath_request(self,model_id, interface_id, parameter_id):
      if not session.get("logged_in"):
          return redirect(url_for("login"))
      parameter_response_one = Parameter.query.filter_by(parameter_id=parameter_id).first()
      edit_parameter_response = ParameterResponseForm()
      submit = SubmitForm()
      if submit.validate_on_submit():
          parameter_response_one.parameter_name = edit_parameter_response.parameter_name.data
          parameter_response_one.necessary = edit_parameter_response.necessary.data
          parameter_response_one.type = edit_parameter_response.type.data
          parameter_response_one.default = edit_parameter_response.default.data
          parameter_response_one.remark = edit_parameter_response.remark.data
          parameter_response_one.parameter_group_id = edit_parameter_response.parameter_group_id.data
          parameter_response_one.level = edit_parameter_response.level.data
          db.session.commit()
          return redirect(url_for("parameter_response",
                                  model_id=model_id,
                                  interface_id=interface_id))
      edit_parameter_response.parameter_name.data = parameter_response_one.parameter_name
      edit_parameter_response.necessary.data = parameter_response_one.necessary
      edit_parameter_response.type.data = parameter_response_one.type
      edit_parameter_response.default.data = parameter_response_one.default
      edit_parameter_response.remark.data = parameter_response_one.remark
      edit_parameter_response.parameter_group_id.data = parameter_response_one.parameter_group_id
      edit_parameter_response.level.data = parameter_response_one.level
      return render_template("editparameter_response.html",
                             model_id=model_id,
                             interface_id=interface_id,
                             parameter_id=parameter_id,
                             edit_parameter_response=edit_parameter_response,
                             submit=submit)
# 删除返回参数
@app.route("/deleteparameter_response/<model_id>&<interface_id>&<parameter_id>", methods=["GET", "POST"])
def deleteparameter_response(model_id, interface_id, parameter_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    deleteparameter_response_one = Parameter.query.filter_by(parameter_id=parameter_id).first()
    db.session.delete(deleteparameter_response_one)
    db.session.commit()
    parameter_response_all = Parameter.query.filter_by(interface_id=interface_id, parameter_type=20).all()
    parameter_response_forms = []
    for i in range(len(parameter_response_all)):
        parameter_response_form = {"parameter_id": parameter_response_all[i].parameter_id,
                                   "parameter_name": parameter_response_all[i].parameter_name,
                                   "necessary": parameter_response_all[i].necessary,
                                   "type": parameter_response_all[i].type,
                                   "default": parameter_response_all[i].default,
                                   "remark": parameter_response_all[i].remark,
                                   "parameter_group_id": parameter_response_all[i].parameter_group_id,
                                   "level": parameter_response_all[i].level}
        parameter_response_forms.append(parameter_response_form)
    return render_template("parameter_response.html",
                           model_id=model_id,
                           interface_id=interface_id,
            parameter_response_forms=parameter_response_forms)
# 用户管理
class UserView(View): 
  methods=["GET", "POST"]
  def dispath_request(self):
      if not session.get("logged_in"):
          return redirect(url_for("login"))
      user_all = User.query.filter_by(status=1).all()
      user_forms = []
      for i in range(len(user_all)):
          user_form = {"user_id": user_all[i].uer_id,
                       "user_name": user_all[i].user_name,
                       "password": user_all[i].password[:30],
                       "status": user_all[i].status,
                       "level": user_all[i].level,
                       "user_zhuce_date": user_all[i].user_zhuce_date,
                       "user_zhuce_email": user_all[i].user_zhuce_email,
                       "user_iphone": user_all[i].user_iphone,
                       "user_qq": user_all[i].user_qq
                       }
          user_forms.append(user_form)
      return render_template("user_admin.html",user_forms=user_forms)
#注册
class Register(View):
  methods=['GET','POST']
  def dispath_request(self):
      form = ReguistForm()
      if form.validate_on_submit():
          user=form.user_name.data
          me=User.query.filter_by(user_name=user).first()
          if me:
              flash('用户名已经存在！')
              return  render_template('regist.html',form=form)
          if form.que_password.data != form.password.data:
              flash(' 确认密码是否一致！')
              return  render_template('regist.html',form=form)
          passw=form.password.data
          print(passw)
          add=User(
              user_name=form.user_name.data,
              status=1,
              user_zhuce_email=form.email.data,
              user_iphone=form.iphone.data,
              user_qq=form.qq.data,
              user_zhuce_date=datetime.datetime.now()
                  )
          add.set_password(password=passw)
          db.session.add(add)
          db.session.commit()
          return  redirect(url_for('login'))
      return render_template("regist.html",
                             form=form)
#删除用户
class DeleteView(View):
  methods=['GET','POST']
  def dispath_request(self,user_name):
      if not session.get("logged_in"):
          return redirect(url_for("login"))
      delete_user=User.query.filter_by(user_name=user_name).first()
      db.session.delete(delete_user)
      db.session.commit()
      user_all = User.query.filter_by(status=1).all()
      user_forms = []
      for i in range(len(user_all)):
          user_form = {"user_id": user_all[i].uer_id,
                       "user_name": user_all[i].user_name,
                       "password": user_all[i].password[:30],
                       "status": user_all[i].status,
                       "level": user_all[i].level,
                       "user_zhuce_date": user_all[i].user_zhuce_date,
                       "user_zhuce_email": user_all[i].user_zhuce_email,
                       "user_iphone": user_all[i].user_iphone,
                       "user_qq": user_all[i].user_qq
                       }
          user_forms.append(user_form)
      return render_template("user_admin.html",
                             user_forms=user_forms)
#编辑用户
class Eidituser(View):
  methods=['GET','POST']
  def dispath_request(self,user_name):
      if not session.get("logged_in"):
          return redirect(url_for("login"))
      edituser_one=User.query.filter_by(user_name=user_name).first()
      editusermodel=ReguistForm()
      submit = SubmitForm()
      if submit.validate_on_submit():
          edituser_one.user_name=editusermodel.user_name.data
          edituser_one.user_zhuce_email=editusermodel.email.data
          edituser_one.user_iphone=editusermodel.iphone.data
          edituser_one.user_qq=editusermodel.qq.data
          db.session.commit()
          return  redirect(url_for('users'))
      editusermodel.user_name.data= edituser_one.user_name
      editusermodel.email.data = edituser_one.user_zhuce_email
      editusermodel.iphone.data =edituser_one.user_iphone
      editusermodel.qq.data=edituser_one.user_qq
      return  render_template('editeruser.html',
                              user_name=user_name,
                              editusermodel=editusermodel,
                              submit=submit)