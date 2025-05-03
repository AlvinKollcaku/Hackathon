import uuid
from DB import db
from sqlalchemy.dialects.postgresql import UUID, JSONB, NUMERIC, TIMESTAMP, TEXT

class EvaluationReport(db.Model):
    __tablename__ = 'evaluation_reports'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tenders.id', ondelete='CASCADE'), nullable=False)
    pdf_url = db.Column(TEXT, nullable=False)
    created_at = db.Column(TIMESTAMP, nullable=False, server_default=db.func.now())
    approved_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    signed_at = db.Column(TIMESTAMP)

    # Relationships
    tender = db.relationship('Tender', back_populates='evaluation_report')
    approver = db.relationship('User', back_populates='evaluation_reports_signed')