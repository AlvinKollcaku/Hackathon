import uuid
from DB import db
from sqlalchemy.dialects.postgresql import UUID, JSONB, NUMERIC, TIMESTAMP, TEXT
from enums import *

class Criterion(db.Model):
    __tablename__ = 'criteria'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tenders.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(TEXT, nullable=False)
    type = db.Column(criterion_type_enum, nullable=False)
    weight_pct = db.Column(NUMERIC(5,2), nullable=False)
    mandatory = db.Column(db.Boolean, nullable=False, default=False)
    max_score = db.Column(db.Integer, nullable=False, default=100)
    position = db.Column(db.SmallInteger, nullable=False, default=1)

    # Relationships
    tender = db.relationship('Tender', back_populates='criteria')
    bid_items = db.relationship('BidItem', back_populates='criterion', cascade='all, delete-orphan')
    scores = db.relationship('Score', back_populates='criterion')