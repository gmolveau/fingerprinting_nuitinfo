from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

api = Blueprint('api', __name__)

# Import any endpoints here to make them available
from . import main

