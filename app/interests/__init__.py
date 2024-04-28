from app import conn
from flask import Blueprint

interests = Blueprint('interests', __name__)

# Import routes
from . import routes
