from . import auth
from flask import render_template,request,url_for,flash
from .. import db

@auth.route('/login')
def login():
  
  return "<h1> you are an auth login</h1>"