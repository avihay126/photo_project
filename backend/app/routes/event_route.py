from flask import Blueprint, request, jsonify
from ..models import Photographer, Event
from .. import db
from flask_jwt_extended import get_jwt_identity, jwt_required
import os
from ..s3_service import get_s3_client, upload_image_to_s3
import requests
import qrcode
import io


event_route = Blueprint('event_route', __name__)

def protected():
    user_id = get_jwt_identity()
    user = Photographer.query.get(user_id)
    return user

@event_route.route('/create-event', methods=['POST'])
@jwt_required()
def create_event():
    user = protected()
    if not user:
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    if not data or not data.get('name') or not data.get('date') or not data.get('location'):
        return jsonify({'message': 'Missing required fields'}), 400
    new_event = Event(
        name=data['name'],
        date=data['date'],
        location=data['location'],
        photographer_id=user.id,
        directory_path=data['name'] + "_" + data['date'],
        qr_path='temp'
    )
    db.session.add(new_event)
    db.session.commit()
    create_event_qr(new_event.id)
    return jsonify({'message': 'Event created successfully'}), 201



@event_route.route('/delete-event/<int:event_id>', methods=['POST'])
@jwt_required()
def delete_event(event_id):
    user = protected()
    if not user:
        return jsonify({'message': 'Unauthorized'}), 401
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'message': 'Event not found'}), 404
    if event.photographer_id != user.id:
        return jsonify({'message': 'Unauthorized'}), 401
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'}), 200


@event_route.route('/get-events', methods=['GET'])
@jwt_required()
def get_events():
    user = protected()
    if not user:
        return jsonify({'message': 'Unauthorized'}), 401
    events = Event.query.filter_by(photographer_id=user.id).all()
    events_list = [{'id': event.id, 'name': event.name, 'date': event.date, 'location': event.location} for event in events]
    return jsonify({'events': events_list}),200



def create_event_qr(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'message': 'Event not found'}), 404
    landing_page_url = f"https://example.com/event/{event_id}" # Replace with the future actual landing page URL
    
    qr = qrcode.make(landing_page_url)
    qr_bytes = io.BytesIO()
    qr.save(qr_bytes, format="PNG")  
    qr_bytes.seek(0) 
    url = upload_image_to_s3(f"qr_codes/{event_id}.png", qr_bytes)
    event.qr_path = url
    db.session.commit()




# @event_route.route('/test', methods=['GET'])
# def upload_image_to_s3():
#     image_url = "https://picsum.photos/200"
#     s3_key = "uploads/image.jpg"
#     s3_client = get_s3_client()
    
#     # הורדת התמונה מהאינטרנט
#     response = requests.get(image_url, stream=True)
#     if response.status_code != 200:
#         raise Exception(f"Failed to fetch image from {image_url}")
    
#     # העלאת התמונה ל-S3
#     try:
#         s3_client.upload_fileobj(
#             response.raw,
#             os.getenv('AWS_BUCKET_NAME'),
#             s3_key,
#         )
#         s3_url = f"https://{os.getenv('AWS_BUCKET_NAME')}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{s3_key}"
#         print(f"Image uploaded successfully to: {s3_url}")
#         return s3_url
#     except Exception as e:
#         print(f"Error uploading to S3: {e}")
#         raise
