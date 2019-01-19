from flask import Blueprint
from flask import render_template
from flask import request
from flask import jsonify

from p5site.utils import form
from p5site.utils.ret import BaseResponse


ac = Blueprint("ac",__name__)


@ac.route('/login',methods = ['POST','GET'])
def login():
    ret = BaseResponse()

    if request.method == 'GET':
        login_form = form.LoginForm()
        return render_template('login.html',form=login_form)

    login_form = form.LoginForm(request.form)
    if login_form.validate():
        return jsonify(ret.dict)
    print(login_form.pwd.errors)
    return render_template('login.html',form=login_form)



@ac.route('/register')
def register():
    return render_template('register.html')