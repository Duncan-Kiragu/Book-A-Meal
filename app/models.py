from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique = True, index = True)
    password = db.Column(db.String)

    role_id = db.relationship('Role', backref='user', lazy ='dynamic')
    order_id = db.relationship('Order', backref='user', lazy='dynamic')



    @property 
    def password(self):
        raise AttributeError('You cannot read password')

    @password.setter
    def password(self,password):
        self.password = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password,password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    def __repr__(self):
        return f'User {self.username}'


class Admin(UserMixin,db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique = True, index = True)
    password = db.Column(db.String)
    bio = db.Column(db.String)
    profile_pic = db.Column(db.String)
    role_id = db.relationship('Role', backref='admin', lazy ='dynamic')
    order_id = db.relationship('Order',backref='admin', lazy='dynamic')

    @property 
    def password(self):
        raise AttributeError('You cannot read password')

    @password.setter
    def password(self,password):
        self.password = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password,password)

    @login_manager.user_loader
    def load_user(admin_id):
        return Admin.query.get(int(admin_id))


    def __repr__(self):
        return f'User {self.username}'



class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    admin_id = db.Column(db.Integer,db.ForeignKey('admins.id'))




class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer,primary_key = True)
    order_name = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    admin_id = db.Column(db.Integer,db.ForeignKey('admins.id'))
    menu_id = db.Column(db.Integer,db.ForeignKey('menu.id'))


    @classmethod
    def get_order(cls,id):
        orders = Order.query.filter_by(order_id = id).all()
        return orders

   

    
    
class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    admin_id = db.Column(db.Integer,db.ForeignKey('admins.id'))
    order_id = db.Column(db.Integer,db.ForeignKey('orders.id'))

    def save_menu(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_menu(cls,id):
        menu = Menu.query.filter_by(menu_id = id).all()
        return menu

	

class Subscriber(db.Model):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer,primary_key = True)
    subscriber_name = db.Column(db.String)
    subscriber_email = db.Column(db.String)

    @classmethod
    def get_subscribers(cls):
        return Subscriber.query.all()



