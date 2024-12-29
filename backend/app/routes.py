from flask import Blueprint, jsonify, request
# from .models import  User, Post
from . import db

bp = Blueprint('main', __name__)

# @bp.route('/items', methods=['GET'])
# def get_items():
#     items = User.query.all()
#     return jsonify([item.to_dict() for item in items]), 200

# @bp.route('/items', methods=['POST'])
# def create_item():
#     data = request.get_json()
#     new_item = User(**data)
#     db.session.add(new_item)
#     db.session.commit()
#     return jsonify(new_item.to_dict()), 201

# @bp.route('/items/<int:item_id>', methods=['GET'])
# def get_item(item_id):
#     item = User.query.get_or_404(item_id)
#     return jsonify(item.to_dict()), 200

# @bp.route('/items/<int:item_id>', methods=['PUT'])
# def update_item(item_id):
#     item = User.query.get_or_404(item_id)
#     data = request.get_json()
#     for key, value in data.items():
#         setattr(item, key, value)
#     db.session.commit()
#     return jsonify(item.to_dict()), 200

# @bp.route('/items/<int:item_id>', methods=['DELETE'])
# def delete_item(item_id):
#     item = User.query.get_or_404(item_id)
#     db.session.delete(item)
#     db.session.commit()
#     return '', 204