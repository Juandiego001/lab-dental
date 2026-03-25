import os
from flask import request
import redis
from pathlib import Path
from flask_cors import CORS
from apiflask import APIFlask
from dotenv import load_dotenv
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

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
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

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

'''Create different folders for files'''
base_route = Path.cwd()

installations_files_folder = "installations_files"
installation_files_full_route = base_route / installations_files_folder
if not installation_files_full_route.exists():
    installation_files_full_route.mkdir(parents=True, exist_ok=True)

equipments_files_folder = "equipments_files"
equipments_full_route = base_route / equipments_files_folder
if not equipments_full_route.exists():
    equipments_full_route.mkdir(parents=True, exist_ok=True)

users_files_folder = "users_files"
users_full_route = base_route / users_files_folder
if not users_full_route.exists():
    users_full_route.mkdir(parents=True, exist_ok=True)

users_files_folder = "manuals_files"
users_full_route = base_route / users_files_folder
if not users_full_route.exists():
    users_full_route.mkdir(parents=True, exist_ok=True)


app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_COOKIE_SECURE"] = ENV == 'production'
app.config['JWT_COOKIE_CSRF_PROTECT'] = ENV == 'production'


def get_locale():
    '''Get locale'''

    supported_languages = ['es', 'en']
    lang_cookie = request.cookies.get('i18n_redirected')
    if lang_cookie:
        return lang_cookie
    return request.accept_languages.best_match(supported_languages)


db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
r = redis.Redis.from_url(REDIS_URL)
babel = Babel(app, locale_selector=get_locale)
