from app import app
from app.auth import auth
from app.pets import pets
from app.apartment import apartment
from app.interests import interests

app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(pets, url_prefix='/pets')
app.register_blueprint(apartment, url_prefix='/apartment')
app.register_blueprint(interests, url_prefix='/interests')

@app.route('/')
def hello_world():
    return 'Hello World'
