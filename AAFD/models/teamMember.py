import uuid
from DB import db
from sqlalchemy.dialects.postgresql import UUID, JSONB, NUMERIC, TIMESTAMP, TEXT

class TeamMember(db.Model):
    __tablename__ = 'team_members'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bid_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bids.id', ondelete='CASCADE'), nullable=False)
    full_name = db.Column(TEXT, nullable=False)
    birth_year = db.Column(db.SmallInteger)
    education = db.Column(TEXT)
    task_assigned = db.Column(TEXT)
    license_info = db.Column(TEXT)
    years_experience = db.Column(db.SmallInteger)
    cv_url = db.Column(TEXT)

    # Relationships
    bid = db.relationship('Bid', back_populates='team_members')