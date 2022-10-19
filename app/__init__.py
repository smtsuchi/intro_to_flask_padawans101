from flask import Flask
from config import Config
from flask_migrate import Migrate
from .models import db

# import blueprint
from .auth.routes import auth

app = Flask(__name__)

app.config.from_object(Config)

# registering your blueprint
app.register_blueprint(auth)



# initialize our database to work with our app
db.init_app(app)
migrate = Migrate(app, db)


from . import routes
from . import models