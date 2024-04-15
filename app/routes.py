from app import app
from app.auth import auth
from app.pets import pets

app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(pets, url_prefix='/pets')

@app.route('/')
def hello_world():
    return 'Hello World'
