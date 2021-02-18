import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__)
    env = os.environ.get('env')
    cfg = 'saws.config.ProdConfig'
    if env == 'LOCAL':
        cfg = 'saws.config.DevConfig'
    app.config.from_object(cfg)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():

        from .blueprints import index
        app.register_blueprint(index.bp)

        from .blueprints import auth
        app.register_blueprint(auth.bp)

        return app


app = create_app()
