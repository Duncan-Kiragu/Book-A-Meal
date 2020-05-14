from flask import render_template, redirect, url_for,flash
from . import auth_admin
from ..models import Admin
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user,login_required
from .. import db


@auth_admin.route('/register1', methods = ['GET', 'POST'])
def register1():
    title = "Sign Up"
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        pass_code = form.password.data
        new_admin = Admin(username = username, email = email, password = pass_code)
        new_admin.save_admin()
        return redirect(url_for('auth_admin.login1'))
    return render_template('auth_admin/register1.html', title = title, registration_form = form)


@auth_admin.route('/login1', methods = ['GET', 'POST'])
def login1():
    title = 'Sign in'
    login_form = LoginForm()
    if login_form.validate_on_submit():
        admin = Admin.query.filter_by(email = login_form.email.data).first()
        if admin is not None and admin.verify_password(login_form.pasword.data):
            login_user(admin, login_form.remember.data)
            return redirect(url_for('main.admin_index', admin = admin))
            flash('Invalid username or password')
    return render_template('auth_admin/login.html', title = title, login_form = login_form)


@auth_admin.route('/logout')
@login_required
def logout():
    logout_admin()
    flash('Successful Log out')
    return redirect(url_for('main.index'))