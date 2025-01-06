from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager


db = SQLAlchemy()

def create_app():
    my_app = Flask(__name__)
    load_dotenv()
    my_app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    

    

    my_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    db.init_app(my_app)
    jwt = JWTManager(my_app)
    my_app.config['JWT_TOKEN_LOCATION'] = ['cookies']

    with my_app.app_context():
        from . import models
        db.create_all()

    from .routes.photographer_route import photographer_routes 
    my_app.register_blueprint(photographer_routes)

    return my_app
