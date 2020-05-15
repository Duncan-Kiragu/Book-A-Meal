from ..models import User,Admin,Role,Order,Menu,Subscriber
from .forms import AddOrder, SubscriberForm,UpdateProfile ,AddMenu 
from .. import db,photos
from . import main
from flask import render_template, redirect, url_for,flash,request,abort
from flask_login import login_required, current_user
from datetime import datetime
from ..email import mail_message
from sqlalchemy import desc


@main.route('/')
def index():
    title = "book-A-Meal"
    subscriber_form = SubscriberForm()
    if subscriber_form.validate_on_submit():
        subscriber_email = subscriber_form.email.data
        new_subscriber = Subscriber(email = subscriber_email)
        new_subscriber.save_subscriber()
        mail_message("Welcome to book-A-Meal", "email/welcome_user", new_subscriber.email)
        return redirect(url_for('main.index'))

    return render_template('index.html',title = title,subscriber_form = subscriber_form)

@main.route('/admin')
def admin_index():
    admin = Admin.query.first()
    return render_template('admin_index.html', admin = admin )


@main.route('/admin/<uname>')
def admin_profile(uname):
    admin = Admin.query.filter_by(username = uname).first()
    if admin is None:
        abort(404)
    return render_template('profile/profile.html', uname = admin.username ,admin = admin)



@main.route('/admin/<uname>/update', methods=['GET','POST'])
@login_required
def update_profile(uname):
    admin = Admin.query.filter_by(username = uname).first()
    if admin is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        admin.bio = form.bio.data
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('main.admin_profile', uname = admin.username))

    return render_template('profile/update.html',admin = admin, form = form)


@main.route('/admin/<uname>/update/pic', methods=['GET','POST'])
@login_required
def update_pic(uname):
    admin = Admin.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        admin.profile_pic = path
        db.session.commit()
    return redirect(url_for('main.admin_profile',uname = admin.username))


@main.route('/new-menu', methods = ['GET','POST'])
@login_required
def new_menu():
    menus = Menu.query.all()
    menu_form = AddMenu()
    if menu_form.validate_on_submit():
        title = menu_form.title.data
        description = menu_form.description.data
        price = menu_form.price.data
        new_menu = Menu(title = title, description = description, price = price)
        new_menu.save_menu()
        return render_template('menu_order/new_menu.html',title = title, menu_form = menu_form, menus = menus)
    title = 'New Menu'
    return render_template('menu_order/new_menu.html', title = title, menu_form = menu_form, menus = menus)



@main.route('/menu/<int:id>', methods = ["GET","POST"])
def menu(id):
    menu = Menu.query.all()
    return render_template('menu.html', menu = menu)


@main.route('/menu/latest', methods = ['GET','POST'])
def latest_menu():
    menu = Menu.query.order_by(desc(Menu.id)).all()

    return render_template('menu.html',menu = menu)



@main.route('/menu/new-menu/<menu_id>', methods = ["GET","POST"])
def admin_menu(menu_id):
    admins = Admin.query.filter_by(menu_id = Menu.id).first()
    return render_template('index.html' ,admins = admins)



@main.route('/menu/<int:id>/update', methods = ['GET','POST'])
@login_required
def update_menu(menu_name):
    form = AddMenu()
    menu = Menu.query.filter_by(menu_name = menu_name).first()
    form.menu.data = menu
    if form.validate_on_submit():
        menu = form.menu.data
        db.session.commit()
        return redirect(url_for('main.menu', id = id))
    elif request.method == 'GET':
        form.menu.data = menu
    return render_template('new_menu.html', form = form, menu_name = menu_name)



@main.route('/menu/delete_menu/<int:id>', methods = ["GET","POST"])
@login_required
def delete_menu(id):
    menu = Menu.query.filter_by(id = id).first()
    db.session.delete(menu)
    db.session.commit()

    flash('Menu has been deleted')

    return redirect(url_for('main.menu',title = title, menu = menu))

@main.route('/menu/order')
@login_required
def get_order():
    orders = Order.query.all()
    return render_template('order.html', orders = orders )


@main.route('/menu/another_order')
@login_required
def another_order():
    return redirect(url_for('main.latest_menu'))


@main.route('/menu/order/checkout')
@login_required
def review_order():
    menus = Menu.query.all()
    user = User.query.first()
    return render_template('checkout.html',menus = menus, user = user)

@main.route('/menu/order/checkout/proceed')
@login_required
def proceed_payment():
    return render_template('final_order.html')

@main.route('/menu/order/checkout/proceed/post')
@login_required
def place_order():
    return render_template('order_message.html')

@main.route('/menu/order/checkout/proceed/cancel')
@login_required
def cancel_order():
    return render_template('cancel.html')

@main.route('/subscription',methods=['GET','POST'])
def subscription():
    subscription_form = SubscriberForm()
    if subscription_form.validate_on_submit():
        new_subscriber = Subscriber(subscriber_name=subscription_form.username.data,subscriber_email=subscription_form.email.data)
        db.session.add(new_subscriber)
        db.session.commit()
        flash('You have successfully subscribed!')
        return redirect(url_for('main.index'))    
    return render_template('subscription.html',subscription_form = subscription_form)


@main.route('/order/<int:id>', methods = ["GET","POST"])
def new_order(id):
    order_name = Order.get_order(id)
    posted_date = menu.posted.strftime('%b %d, %Y')
    return render_template('order.html', order_name = order_name, date = posted_date)


@main.route('/menu/delete_menu/<int:id>', methods = ["GET","POST"])
@login_required
def delete_order(id):
    order = Order.query.filter_by(id = order_id).first()
    db.session.delete(order)
    db.session.commit()

    flash('Order has been deleted')

    return redirect(url_for('main.new_order',title = title, order = order))