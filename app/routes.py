from app import app
from app.auth import routes

@app.route('/')
def hello_world():
    return 'Hello World'
