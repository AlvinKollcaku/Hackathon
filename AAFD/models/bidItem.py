import uuid
from DB import db
from sqlalchemy.dialects.postgresql import UUID, JSONB, NUMERIC, TIMESTAMP, TEXT

class BidItem(db.Model):
    __tablename__ = 'bid_items'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bid_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bids.id', ondelete='CASCADE'), nullable=False)
    criterion_id = db.Column(UUID(as_uuid=True), db.ForeignKey('criteria.id', ondelete='CASCADE'), nullable=False)
    value_text = db.Column(TEXT)
    value_numeric = db.Column(NUMERIC(18,2))
    file_url = db.Column(TEXT)

    # Relationships
    bid = db.relationship('Bid', back_populates='bid_items')
    criterion = db.relationship('Criterion', back_populates='bid_items')