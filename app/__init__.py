from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_options
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_uploads import UploadSet,configure_uploads,IMAGES


db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
mail = Mail()
photos = UploadSet('photos',IMAGES)

def create_app(config_name):
    app = Flask(__name__)

    #Creating app configurations
    app.config.from_object(config_options[config_name])
   

    #Registers the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth_user import auth_user as auth_user_blueprint
    app.register_blueprint(auth_user_blueprint, url_prefix = '/authenticate')
    
    from .auth_admin import auth_admin as auth_admin_blueprint
    app.register_blueprint(auth_admin_blueprint, url_prefix = '/authenticate')


    #Initializing flask extensions
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    configure_uploads(app,photos)


    return app