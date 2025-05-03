import uuid
from DB import db
from sqlalchemy.dialects.postgresql import UUID, JSONB, NUMERIC, TIMESTAMP, TEXT

class VendorContract(db.Model):
    __tablename__ = 'vendor_contracts'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bid_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bids.id', ondelete='CASCADE'), nullable=False)
    contract_title = db.Column(TEXT, nullable=False)
    role = db.Column(TEXT)
    value_usd = db.Column(NUMERIC(18,2))
    investor_name = db.Column(TEXT)
    contact_details = db.Column(TEXT)
    start_date = db.Column(db.Date)
    completion_date = db.Column(db.Date)
    description = db.Column(TEXT)

    # Relationships
    bid = db.relationship('Bid', back_populates='vendor_contracts')