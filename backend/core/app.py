import os
from pathlib import Path
from flask_cors import CORS
from apiflask import APIFlask
from dotenv import load_dotenv
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

ENV = os.getenv('ENV') or 'development'
HOST = os.getenv('HOST') or 'localhost'
PORT = int(os.getenv('PORT') or 5000)
MAIL_USER = os.getenv('MAIL_USER')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_SENDER = os.getenv('MAIL_SENDER')
MAIL_SERVER = os.getenv('MAIL_SERVER')
FRONTEND_APP_BASE_URL = os.getenv(
    'FRONTEND_APP_BASE_URL', 'http://localhost:3000')

app = APIFlask(__name__, title='SOE Latam API', version='0.0.1', enable_openapi=ENV ==
               'development', template_folder='../templates', json_errors=False)
app.security_schemes = {
    'BearerAuth': {
        'type': 'http',
        'scheme': 'bearer',
        'bearerFormat': 'JWT',
    }
}

CORS(app)

app.config['JWT_SECRET_KEY'] = 'fB7Cp8UoZJ6FQIG0DjLjes5E'

'''Create folder files_data'''
base_route = Path.cwd() 
files_data_folder = "files_data"
full_route = base_route / files_data_folder
if not full_route.exists():
    full_route.mkdir(parents=True, exist_ok=True)


if ENV == 'development':
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
else:
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
