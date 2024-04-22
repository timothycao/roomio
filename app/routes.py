from app import app
from app.auth import auth
from app.pets import pets
from app.apartment import apartment

app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(pets, url_prefix='/pets')
app.register_blueprint(apartment, url_prefix='/apartment')

@app.route('/')
def hello_world():
    return 'Hello World'
