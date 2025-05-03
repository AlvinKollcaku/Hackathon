from flask import request, jsonify, abort
from flask_smorest import Blueprint
from models import Attachment
from DB import db
from schemas import AttachmentSchema
from google_drive import upload_file_to_drive
import io

attachments_bp = Blueprint("attachments", __name__, url_prefix="/attachments")

# Marshmallow schemas
attachment_schema = AttachmentSchema()
attachments_schema = AttachmentSchema(many=True)

@attachments_bp.route("", methods=["POST"])
def upload_attachment():
    # 1. Ensure a file is present
    if "file" not in request.files:
        abort(400, "No file part in the request")
    file = request.files["file"]

    # 2. Get owner info from form
    owner_type = request.form.get("owner_type")
    owner_id   = request.form.get("owner_id")
    if not owner_type or not owner_id:
        abort(400, "owner_type and owner_id are required")

    # 3. Upload to Drive
    stream = io.BytesIO(file.read())
    stream.seek(0)
    public_url = upload_file_to_drive(stream, file.filename, file.mimetype)

    # 4. Save record
    attachment = Attachment(
        owner_type=owner_type,
        owner_id=owner_id,
        file_name=file.filename,
        file_url=public_url
    )
    db.session.add(attachment)
    db.session.commit()

    return jsonify(attachment_schema.dump(attachment)), 201

@attachments_bp.route("", methods=["GET"])
def list_attachments():
    all_ = Attachment.query.all()
    return jsonify(attachments_schema.dump(all_)), 200

@attachments_bp.route("/<uuid:attachment_id>", methods=["GET"])
def get_attachment(attachment_id):
    att = Attachment.query.get_or_404(attachment_id)
    return jsonify(attachment_schema.dump(att)), 200
