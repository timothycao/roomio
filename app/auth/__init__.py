from app import app, conn
from flask import Blueprint
from flask_bcrypt import Bcrypt

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

auth = Blueprint('auth', __name__)

# Import routes
from . import routes
