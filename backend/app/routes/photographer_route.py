from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from ..models import Photographer, RefreshToken
from .. import db
import uuid

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
    
    access_token = create_access_token(identity=str(user.id))
    refresh_token = str(uuid.uuid4())
    refresh_entry = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    try:
        db.session.add(refresh_entry)
        db.session.commit()
        response = jsonify({"message": "Login successful"})
        response.set_cookie('access_token_cookie', access_token, httponly=True)
        response.set_cookie('refresh_token_cookie', refresh_token, httponly=True)
        return response, 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@photographer_routes.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = Photographer.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": f"Welcome, {user.name}!"}), 200




@photographer_routes.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.cookies.get('refresh_token_cookie')

    if not refresh_token:
        return jsonify({"error": "No refresh token provided"}), 401

    token_entry = RefreshToken.query.filter_by(token=refresh_token).first()
    if not token_entry or token_entry.expires_at < datetime.utcnow():
        return jsonify({"error": "Invalid or expired refresh token"}), 401

    access_token = create_access_token(identity=token_entry.user_id)
    response = jsonify({"message": "Token refreshed successfully"})
    response.set_cookie('access_token_cookie', access_token, httponly=True)
    return response, 200





@photographer_routes.route('/logout', methods=['POST'])
def logout():
    refresh_token = request.cookies.get('refresh_token_cookie')

    if refresh_token:
        token_entry = RefreshToken.query.filter_by(token=refresh_token).first()
        if token_entry:
            db.session.delete(token_entry)
            db.session.commit()

    response = jsonify({"message": "Logout successful"})
    response.delete_cookie('access_token_cookie')
    response.delete_cookie('refresh_token_cookie')
    return response, 200
