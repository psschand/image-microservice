from app import db
from datetime import datetime

class ImageMetadata(db.Model):
    __tablename__ = 'image_metadata'

    id = db.Column(db.String, primary_key=True)
    file_ext = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

