from flask import Blueprint, request, jsonify, abort
from models import Attachment
from DB import db
from schemas import AttachmentSchema


# Blueprint for attachments
attachments_bp = Blueprint('attachments', __name__, url_prefix='/attachments')

# Schemas
attachment_schema = AttachmentSchema()
attachments_schema = AttachmentSchema(many=True)

@attachments_bp.route('', methods=['GET'])
def list_attachments():
    """List all attachments"""
    files = Attachment.query.order_by(Attachment.created_at.desc()).all()
    return jsonify(attachments_schema.dump(files)), 200

@attachments_bp.route('', methods=['POST'])
def create_attachment():
    """Create a new attachment"""
    data = request.get_json() or {}
    try:
        file = attachment_schema.load(data, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.add(file)
    db.session.commit()
    return jsonify(attachment_schema.dump(file)), 201

@attachments_bp.route('/<uuid:att_id>', methods=['GET'])
def get_attachment(att_id):
    """Fetch an attachment by ID"""
    file = Attachment.query.get_or_404(att_id)
    return jsonify(attachment_schema.dump(file)), 200

@attachments_bp.route('/<uuid:att_id>', methods=['PUT'])
def replace_attachment(att_id):
    """Replace an existing attachment entirely"""
    file = Attachment.query.get_or_404(att_id)
    data = request.get_json() or {}
    try:
        updated = attachment_schema.load(data, instance=file, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(attachment_schema.dump(updated)), 200

@attachments_bp.route('/<uuid:att_id>', methods=['PATCH'])
def update_attachment(att_id):
    """Partially update an attachment"""
    file = Attachment.query.get_or_404(att_id)
    data = request.get_json() or {}
    try:
        updated = attachment_schema.load(data, instance=file, session=db.session, partial=True)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(attachment_schema.dump(updated)), 200

@attachments_bp.route('/<uuid:att_id>', methods=['DELETE'])
def delete_attachment(att_id):
    """Delete an attachment"""
    file = Attachment.query.get_or_404(att_id)
    db.session.delete(file)
    db.session.commit()
    return '', 204