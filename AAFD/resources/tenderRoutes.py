from flask.views           import MethodView
from flask_smorest         import abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from flask import request, jsonify

import io
from DB       import db
from models   import Tender, Attachment, Bid
from schemas  import (
    PlainTenderSchema, TenderSchema,
    PlainAttachmentSchema, AttachmentSchema, BidSchema
)
from utils import proc_officer_required
from google_drive import upload_file_to_drive


bp = Blueprint('tenders', __name__, url_prefix='/tenders')

#
# 1) List & publish tenders
#
@bp.route('')
class TenderList(MethodView):
    @bp.response(200, TenderSchema(many=True))
    def get(self):
        """List all tenders"""
        return Tender.query.all()

    #@jwt_required()
    @bp.arguments(PlainTenderSchema)
    @bp.response(201, TenderSchema)
    def post(self, tender_data):
        """Publish a new tender"""
        # Get user ID from JWT
        proc_officer_required()
        current_user_id = get_jwt_identity()

        # Create tender with user ID
        tender = Tender(
            **tender_data,
            created_by=current_user_id
        )

        db.session.add(tender)
        db.session.commit()
        return tender

#
# 2) Retrieve, update (including deadlines), delete a tender
#
@bp.route('/<uuid:tender_id>')
class TenderDetail(MethodView):

    @bp.response(200, TenderSchema)
    def get(self, tender_id):
        """Get a single tender"""
        #Anyone can access the tenders
        return Tender.query.get_or_404(tender_id)

    @bp.arguments(PlainTenderSchema)
    @bp.response(200, TenderSchema)
    def put(self, tender_data, tender_id):
        """Update title, description, publish_at, close_at, ceiling_fund, status, etc."""
        #proc_officer_required()
        tender = Tender.query.get_or_404(tender_id)
        for key, val in tender_data.items():
            setattr(tender, key, val)
        db.session.commit()
        return tender

    def delete(self, tender_id):
        """Remove a draft tender"""
        #proc_officer_required()
        tender = Tender.query.get_or_404(tender_id)
        db.session.delete(tender)
        db.session.commit()
        return '', 204

#
# 3) Attach signed PDFs and other docs to a tender
#
attachment_schema = AttachmentSchema()

@bp.route("/<uuid:tender_id>/attachments", methods=["POST"])
def upload_tender_attachment(tender_id):
    # 1) ensure tender exists
    tender = Tender.query.get_or_404(tender_id)

    # 2) check file in request
    if "file" not in request.files:
        abort(400, "No file part in the request")
    file = request.files["file"]

    # 3) stream it into Google Drive
    stream = io.BytesIO(file.read())
    stream.seek(0)
    public_url = upload_file_to_drive(stream, file.filename, file.mimetype)

    # 4) save in attachments table
    attachment = Attachment(
        owner_type="tender",
        owner_id=tender_id,
        file_name=file.filename,
        file_url=public_url
    )
    db.session.add(attachment)
    db.session.commit()

    # 5) return the new record
    return jsonify(attachment_schema.dump(attachment)), 201

@bp.route('/<uuid:tender_id>/attachments')
class TenderAttachments(MethodView):

    @bp.response(200, AttachmentSchema(many=True))
    def get(self, tender_id):
        """List all attachments for this tender"""
        #proc_officer_required()
        return Attachment.query.filter_by(owner_type='tender', owner_id=tender_id).all()

#
# 4) Notify (award) a winning vendor
#
class WinnerSchema(Schema):
    vendor_id = fields.UUID(required=True)

@bp.route('/<uuid:tender_id>/award')
class TenderAward(MethodView):

    @bp.arguments(WinnerSchema)
    @bp.response(200, TenderSchema)
    def post(self, data, tender_id):
        """
        Mark one bid as awarded and notify the vendor.
        """
        #proc_officer_required()
        # find the bid
        bid = Bid.query.filter_by(tender_id=tender_id, vendor_id=data['vendor_id']).first_or_404()
        bid.status = 'awarded'
        # also close the tender
        tender = bid.tender
        tender.status = 'closed'
        db.session.commit()
        # (you could add actual email/notification logic here)
        return tender
#
# 5) Close the process without awarding
#
@bp.route('/<uuid:tender_id>/close')
class TenderClose(MethodView):

    @bp.response(200, TenderSchema)
    def post(self, tender_id):
        """
        Close the tender process.
        """
        #proc_officer_required()
        tender = Tender.query.get_or_404(tender_id)
        tender.status = 'closed'
        db.session.commit()
        return tender

# Get all bid for a specific tender
@bp.route('/<uuid:tender_id>/bids')
class TenderBids(MethodView):
    @bp.response(200, BidSchema(many=True))
    def get(self, tender_id):
        """List all bids for a specific tender"""
        #proc_officer_required()
        tender = Tender.query.get_or_404(tender_id)
        return tender.bids

