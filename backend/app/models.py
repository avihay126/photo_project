from . import db
import numpy as np
from .Constants import THRESHOLD

class Photographer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    
class RefreshToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('photographer.id'), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    directory_path = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    qr_path = db.Column(db.String(255), nullable=False)
    photographer_id = db.Column(db.Integer, db.ForeignKey('photographer.id'), nullable=False)
    photographer = db.relationship('Photographer', backref=db.backref('events', lazy=True))
    is_open = db.Column(db.Boolean, default=True)

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    event = db.relationship('Event', backref=db.backref('guests', lazy=True))
    stage = db.Column(db.Integer, default=0)

class SelfieImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selfi_encode = db.Column(db.LargeBinary, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    guest = db.relationship('Guest', backref=db.backref('selfie_image', uselist=False))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    event = db.relationship('Event', backref=db.backref('selfie_images', lazy=True))

    def set_encoding(self, encoding_array):
        self.selfi_encode = np.array(encoding_array, dtype=np.float32).tobytes()

    def get_encoding(self):
        return np.frombuffer(self.selfi_encode, dtype=np.float32)

class EventImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    event = db.relationship('Event', backref=db.backref('event_event_images', lazy=True))
    is_classified = db.Column(db.Boolean, default=False)

class ImageGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    face_encode = db.Column(db.LargeBinary, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=True)
    guest = db.relationship('Guest', backref=db.backref('image_groups', lazy=True))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    event = db.relationship('Event', backref=db.backref('event_image_groups', lazy=True))

    def set_encoding(self, encoding_array):
        self.face_encode = np.array(encoding_array, dtype=np.float32).tobytes()

    def get_encoding(self):
        return np.frombuffer(self.face_encode, dtype=np.float32)

    def is_same_person(self, other_face_encode, threshold=THRESHOLD):
        distance = np.linalg.norm(self.get_encoding() - other_face_encode)
        print(f"Distance: {distance}")
        return distance < threshold

class EventImageToImageGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_image_id = db.Column(db.Integer, db.ForeignKey('event_image.id'), nullable=False)
    event_image = db.relationship('EventImage', backref=db.backref('event_image_to_groups', lazy=True))
    image_group_id = db.Column(db.Integer, db.ForeignKey('image_group.id'), nullable=False)
    image_group = db.relationship('ImageGroup', backref=db.backref('image_group_to_event_images', lazy=True))
    sent = db.Column(db.Boolean, default=False)