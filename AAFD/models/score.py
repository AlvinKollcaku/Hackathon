import uuid
from DB import db
from sqlalchemy.dialects.postgresql import UUID, JSONB, NUMERIC, TIMESTAMP, TEXT

class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bid_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bids.id', ondelete='CASCADE'), nullable=False)
    criterion_id = db.Column(UUID(as_uuid=True), db.ForeignKey('criteria.id', ondelete='CASCADE'), nullable=False)
    evaluator_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    ai_suggested = db.Column(NUMERIC(6,2))
    evaluator_score = db.Column(NUMERIC(6,2))
    final_score = db.Column(NUMERIC(6,2))
    comment = db.Column(TEXT)

    __table_args__ = (db.UniqueConstraint('bid_id','criterion_id','evaluator_id', name='_score_uc'),)

    # Relationships
    bid = db.relationship('Bid', back_populates='scores')
    criterion = db.relationship('Criterion', back_populates='scores')
    evaluator = db.relationship('User', back_populates='scores')