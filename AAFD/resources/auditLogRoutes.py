from flask import Blueprint, request, jsonify, abort
from models import AuditLog
from schemas import AuditLogSchema
from DB import db

# Blueprint for audit logs
audit_bp = Blueprint('audit_logs', __name__, url_prefix='/audit_logs')

# Schemas
audit_schema = AuditLogSchema()
audits_schema = AuditLogSchema(many=True)

@audit_bp.route('', methods=['GET'])
def list_audit_logs():
    """List all audit log entries"""
    logs = AuditLog.query.order_by(AuditLog.ts.desc()).all()
    return jsonify(audits_schema.dump(logs)), 200

@audit_bp.route('', methods=['POST'])
def create_audit_log():
    """Create a new audit log entry"""
    data = request.get_json() or {}
    try:
        log = audit_schema.load(data, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.add(log)
    db.session.commit()
    return jsonify(audit_schema.dump(log)), 201

@audit_bp.route('/<int:log_id>', methods=['GET'])
def get_audit_log(log_id):
    """Fetch an audit log entry by ID"""
    log = AuditLog.query.get_or_404(log_id)
    return jsonify(audit_schema.dump(log)), 200

@audit_bp.route('/<int:log_id>', methods=['DELETE'])
def delete_audit_log(log_id):
    """Delete an audit log entry"""
    log = AuditLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    return '', 204