import uuid
from DB import db
from sqlalchemy.dialects.postgresql import UUID, JSONB, NUMERIC, TIMESTAMP, TEXT
from enums import *

class VendorCompany(db.Model):
    __tablename__ = 'vendor_companies'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    legal_name = db.Column(TEXT, nullable=False)
    vat_number = db.Column(TEXT, unique=True)
    country = db.Column(TEXT)
    created_at = db.Column(TIMESTAMP, nullable=False, server_default=db.func.now())

    # Relationships
    users = db.relationship('User', back_populates='vendor')
    bids = db.relationship('Bid', back_populates='vendor')