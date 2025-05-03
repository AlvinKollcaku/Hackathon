import uuid
from DB import db
from sqlalchemy.dialects.postgresql import UUID, JSONB, NUMERIC, TIMESTAMP, TEXT
from enums import *

class Bid(db.Model):
    __tablename__ = 'bids'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tenders.id', ondelete='CASCADE'), nullable=False)
    vendor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('vendor_companies.id', ondelete='CASCADE'), nullable=False)
    submitted_at = db.Column(TIMESTAMP, nullable=False, server_default=db.func.now())
    status = db.Column(bid_status_enum, nullable=False, default='submitted')
    total_price = db.Column(NUMERIC(18,2))
    total_ai_score = db.Column(NUMERIC(6,2))
    total_final_score = db.Column(NUMERIC(6,2))

    __table_args__ = (db.UniqueConstraint('tender_id','vendor_id', name='_tender_vendor_uc'),)

    # Relationships
    tender = db.relationship('Tender', back_populates='bids')
    vendor = db.relationship('VendorCompany', back_populates='bids')
    bid_items = db.relationship('BidItem', back_populates='bid', cascade='all, delete-orphan')
    scores = db.relationship('Score', back_populates='bid', cascade='all, delete-orphan')
    team_members = db.relationship('TeamMember', back_populates='bid', cascade='all, delete-orphan')
    vendor_contracts = db.relationship('VendorContract', back_populates='bid', cascade='all, delete-orphan')