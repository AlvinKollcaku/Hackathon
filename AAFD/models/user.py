import uuid
from DB import db
from sqlalchemy.dialects.postgresql import UUID, JSONB, NUMERIC, TIMESTAMP, TEXT
from enums import *

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = db.Column(TEXT, nullable=False)
    email = db.Column(TEXT, unique=True, nullable=False)
    password_hash = db.Column(TEXT, nullable=False)
    role = db.Column(user_role_enum, nullable=False)
    created_at = db.Column(TIMESTAMP, nullable=False, server_default=db.func.now())
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    vendor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('vendor_companies.id'))

    # Relationships
    vendor = db.relationship('VendorCompany', back_populates='users')
    tenders_created = db.relationship('Tender', back_populates='creator')
    scores = db.relationship('Score', back_populates='evaluator')
    evaluation_reports_signed = db.relationship('EvaluationReport', back_populates='approver')