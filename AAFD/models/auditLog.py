from DB import db
from sqlalchemy.dialects.postgresql import UUID, JSONB, NUMERIC, TIMESTAMP, TEXT

class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    id = db.Column(db.BigInteger, primary_key=True)
    actor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    action = db.Column(TEXT, nullable=False)
    entity_type = db.Column(TEXT, nullable=False)
    entity_id = db.Column(UUID(as_uuid=True))
    ts = db.Column(TIMESTAMP, nullable=False, server_default=db.func.now())
    diff = db.Column(JSONB)