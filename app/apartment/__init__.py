from app import conn
from flask import Blueprint

apartment = Blueprint('apartment', __name__)

# Import routes
from . import routes
