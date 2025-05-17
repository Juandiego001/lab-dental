import os
from dotenv import load_dotenv
from apiflask import APIFlask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

load_dotenv()

ENV = os.getenv('ENV') or 'development'
HOST = os.getenv('HOST') or 'localhost'
PORT = int(os.getenv('PORT') or 5000)

app = APIFlask(__name__, title='Cinema API', version='0.0.1', enable_openapi=ENV == 'development')
CORS(app)

app.config['JWT_SECRET_KEY'] = 'super-secret987'  # Change this!
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
