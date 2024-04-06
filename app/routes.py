from app import app
from app.auth import routes as auth_routes

@app.route('/')
def hello_world():
    return 'Hello World'
