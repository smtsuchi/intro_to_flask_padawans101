from flask import Flask
from config import Config

# import blueprint
from .auth.routes import auth

app = Flask(__name__)

app.config.from_object(Config)

# registering your blueprint
app.register_blueprint(auth)


from . import routes
