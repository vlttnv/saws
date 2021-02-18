import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:{}@podistro-db.cc1k6psptwhw.eu-central-1.rds.amazonaws.com:5432/podistro'.format(
        os.environ.get('DB_PASSWORD')
    )


class DevConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:example@localhost:5432/saws'
