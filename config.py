import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://brendawanjiku:brenda@localhost/meal'
    SECRET_KEY = 'brenda_wanjiku'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
     
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://brendawanjiku:brenda@localhost/meal'
    DEBUG = True


config_options = {
    'development' : DevConfig,
    'production'  : ProdConfig
}