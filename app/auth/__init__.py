from app import app, conn
from flask_bcrypt import Bcrypt

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

# Import routes
from . import routes
