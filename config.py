import os

class Config:
  '''
  config class to be inheritted by other class
  '''

class ProdConfig(Config):
  '''
  production config class
  '''

class DevConfig(Config):
  '''
  development config class
  '''
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://username:password@localhost/sendit'
  ##change the username to your username and password


class TestConfig(Config):
  '''
  tests config class
  '''

config_options = {
  'development': DevConfig,
  'production': ProdConfig,
  'tests': TestConfig
}