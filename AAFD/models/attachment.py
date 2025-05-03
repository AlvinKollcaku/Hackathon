import uuid
from DB import db
from sqlalchemy.dialects.postgresql import UUID, JSONB, NUMERIC, TIMESTAMP, TEXT

class Attachment(db.Model):
    __tablename__ = 'attachments'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_type = db.Column(TEXT)
    owner_id = db.Column(UUID(as_uuid=True))
    file_name = db.Column(TEXT)
    file_url = db.Column(TEXT)
    created_at = db.Column(TIMESTAMP, nullable=False, server_default=db.func.now())



