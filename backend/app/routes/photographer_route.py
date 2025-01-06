from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, 
    jwt_required, 
    get_jwt_identity, 
    set_access_cookies,
    unset_jwt_cookies
)
from datetime import timedelta
from ..models import Photographer
from .. import db

photographer_routes = Blueprint('photographer_routes', __name__)

@photographer_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('name') or not data.get('password') or not data.get('email') or not data.get('phone'):
        return jsonify({"error": "Missing required fields"}), 400

    if Photographer.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(data['password'])
    new_user = Photographer(
        name=data['name'],
        password=hashed_password,
        email=data['email'],
        phone=data['phone']
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Photographer registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@photographer_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing email or password"}), 400

    user = Photographer.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Invalid email or password"}), 401
    
    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))

    response = jsonify({"message": "Login successful"})
    set_access_cookies(response, access_token)
    return response, 200
    

@photographer_routes.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = Photographer.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": f"Welcome, {user.name}!"}), 200



@photographer_routes.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200
