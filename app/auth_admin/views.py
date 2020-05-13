from flask import render_template, redirect, url_for,flash
from . import auth
from ..models import User
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user,login_required
from .. import db
from ..email import mail_message


@auth.route('/register', methods = ['GET', 'POST'])
def register():
    title = "Sign Up"
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        pass_code = form.password.data

        new_user = User(username = username, email = email, password = pass_code)
        new_user.save_user()
        mail_message("Welcome", "email/welcome_user", new_user.email, username = username)

        return redirect(url_for('auth.login'))


    return render_template('auth/register.html', title = title, registration_form = form)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    title = 'Sign in'

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        
        if user is not None and user.verify_password(login_form.pasword.data):
            login_user(user, login_form.remember.data)
            return redirect(url_for('main.index', user = user))
            flash('Invalid username or password')
    
    return render_template('auth/login.html', title = title, login_form = login_form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successful Log out')
    return redirect(url_for('main.index'))