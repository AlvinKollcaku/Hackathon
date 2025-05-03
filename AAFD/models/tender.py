import uuid
from DB import db
from sqlalchemy.dialects.postgresql import UUID, JSONB, NUMERIC, TIMESTAMP, TEXT
from enums import *

class Tender(db.Model):
    __tablename__ = 'tenders'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = db.Column(TEXT, unique=True)
    title = db.Column(TEXT, nullable=False)
    description = db.Column(TEXT)
    publish_at = db.Column(TIMESTAMP)
    deadline = db.Column(TIMESTAMP)
    budget = db.Column(NUMERIC(18,2))
    status = db.Column(tender_status_enum, nullable=False, default='draft')
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(TIMESTAMP, nullable=False, server_default=db.func.now())

    # Relationships
    creator = db.relationship('User', back_populates='tenders_created')
    criteria = db.relationship('Criterion', back_populates='tender', cascade='all, delete-orphan')
    bids = db.relationship('Bid', back_populates='tender', cascade='all, delete-orphan')
    evaluation_report = db.relationship('EvaluationReport', back_populates='tender', uselist=False)