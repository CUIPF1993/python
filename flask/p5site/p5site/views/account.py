from flask import Blueprint
from flask import render_template

from p5site.utils import form

ac = Blueprint("ac",__name__)


@ac.route('/login')
def login():
    login_form = form.LoginForm()
    return render_template('login.html',form=login_form)

@ac.route('/register')
def register():
    return render_template('register.html')