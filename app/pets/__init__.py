from app import conn
from flask import Blueprint

pets = Blueprint('pets', __name__)

# Import routes
from . import routes
