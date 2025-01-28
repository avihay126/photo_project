from flask import Blueprint, request, jsonify
from .photographer_route import protected
from ..models import EventImage
from .. import db
from flask_jwt_extended import  jwt_required

uploader_routes = Blueprint('uploader_routes', __name__)

@uploader_routes.route('/save-image-keys', methods=['POST'])
@jwt_required()
def save_image_keys(): # event_id, urls
    user = protected()
    if not user:
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    if not data or not data.get('event_id') or not data.get('urls'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    urls = data.get('urls')
    event_id = data.get('event_id')
    
    if not isinstance(urls, list) or len(urls) == 0:
        return jsonify({'message': 'Invalid or empty URL list'}), 400

    try:
        images = [EventImage(path=url, event_id=event_id) for url in urls]
        
        db.session.add_all(images)
        db.session.commit()
        

        return jsonify({'message': 'Images saved successfully', 'count': len(images)}), 201

    except Exception as e:
        db.session.rollback()  
        return jsonify({'message': f'Error saving images: {str(e)}'}), 500