from app import app
from app.auth import auth

app.register_blueprint(auth, url_prefix='/')

@app.route('/')
def hello_world():
    return 'Hello World'
