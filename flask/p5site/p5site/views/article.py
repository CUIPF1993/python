from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request




art = Blueprint("art",__name__)


@art.route('/index')
def intdex():
    return render_template('index.html')



@art.route('/articles')
def articles():
    return render_template('articles.html')