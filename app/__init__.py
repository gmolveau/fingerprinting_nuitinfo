from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projet.db'
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "mysecretkey")

    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    with app.app_context():
    	db.create_all()

    return app
