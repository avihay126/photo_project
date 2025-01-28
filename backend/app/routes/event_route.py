from flask import Blueprint, request, jsonify
from ..models import Photographer, Event
from .. import db
from flask_jwt_extended import  jwt_required
import os
from ..s3_service import get_s3_client, upload_image_to_s3
import requests
import qrcode
import io
from .photographer_route import protected


event_route = Blueprint('event_route', __name__)



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
    create_event_qr(new_event)
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



def create_event_qr(event):
    if event is None:
        return jsonify({'message': 'Event not found'}), 404
    landing_page_url = f"https://example.com/event/{event.id}" # Replace with the future actual landing page URL
    
    qr = qrcode.make(landing_page_url)
    qr_bytes = io.BytesIO()
    qr.save(qr_bytes, format="PNG")  
    qr_bytes.seek(0) 
    url = upload_image_to_s3(f"qr_codes/{event.id}.png", qr_bytes)
    event.qr_path = url
    db.session.commit()

    