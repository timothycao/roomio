from flask_bcrypt import Bcrypt
from app import app

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)
