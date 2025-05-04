from datetime import datetime

from flask.views           import MethodView
from flask_smorest         import abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from flask import request, jsonify

import io

from sqlalchemy.exc import SQLAlchemyError

from DB       import db
from models   import Tender, Attachment, Bid
from schemas  import (
    PlainTenderSchema, TenderSchema,
    PlainAttachmentSchema, AttachmentSchema, BidSchema
)
from roleBased import proc_officer_required
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
        #proc_officer_required()
        return Tender.query.all()

    #@jwt_required()
    @bp.arguments(PlainTenderSchema)  # only pulls title, description, deadline, budget
    @bp.response(201, TenderSchema)
    def post(self, tender_data):
        """Create & publish a tender; optionally upload a file at the same time."""
        print("Heloooooooooo")
        try:
            user_id = "22222222-2222-2222-2222-222222222222"
            print(tender_data)

            # 1) Build the Tender with published status + timestamp
            tender = Tender(
                **tender_data,
                created_at=datetime.utcnow(),
                created_by=user_id,
            )
            db.session.add(tender)
            db.session.flush()  # so tender.id exists below

            # 2) If the client also sent a file in multipart/form-data, handle it now
            if 'file' in request.files:
                file = request.files['file']
                stream = io.BytesIO(file.read())
                stream.seek(0)
                public_url = upload_file_to_drive(
                    stream, file.filename, file.mimetype
                )

                attachment = Attachment(
                    owner_type='tender',
                    owner_id=tender.id,
                    file_name=file.filename,
                    file_url=public_url
                )
                db.session.add(attachment)

            db.session.commit()
            return tender
        except Exception as e:
            print("Error creating tender:", str(e))  # Log any exceptions
            db.session.rollback()
            abort(422, description=str(e))

#
# 2) Retrieve, update (including deadlines), delete a tender
#
@bp.route('/<uuid:tender_id>')
class TenderDetail(MethodView):

    @bp.response(200, TenderSchema)
    def get(self, tender_id):
        """Get a single tender"""

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

import uuid

# Get all bid for a specific tender
@bp.route("/<uuid:tender_id>/bids")
class TenderBids(MethodView):

    @bp.response(200, BidSchema(many=True))
    def get(self, tender_id):
        """List all bids for a specific tender."""
        tender = Tender.query.get_or_404(tender_id)
        return tender.bids

    @bp.response(201, BidSchema)
    def post(self, tender_id):
        """
        Create a new bid record for this tender.
        Expects JSON: { "vendor_id": "<uuid-of-vendor>" }
        """
        data = request.get_json() or {}
        vendor_id = '11111111-1111-1111-1111-111111111111'
        # ensure the tender exists
        Tender.query.get_or_404(tender_id)

        # create the Bid (we’re skipping amount & auth for now)
        bid = Bid(
            tender_id=tender_id,
            vendor_id=vendor_id
        )
        db.session.add(bid)
        db.session.commit()

        return bid
#---------------------------------

@bp.route("/<uuid:tender_id>/attachments/tender")
class TenderOnlyAttachments(MethodView):

    @bp.response(200, AttachmentSchema(many=True))
    def get(self, tender_id):
        """For procurement_officer & vendor: just the original tender files."""
        return (
            Attachment.query
            .filter_by(owner_type="tender", owner_id=tender_id)
            .order_by(Attachment.created_at.desc())
            .all()
        )


@bp.route("/<uuid:tender_id>/bids/<uuid:bid_id>/attachments")
class BidAttachments(MethodView):

    @bp.response(200, AttachmentSchema(many=True))
    def get(self, tender_id, bid_id):
        """For a vendor (or evaluator) to list attachments of a _specific_ bid."""
        # you might later check that bid.tender_id == tender_id
        return (
            Attachment.query
            .filter_by(owner_type="bid", owner_id=bid_id)
            .order_by(Attachment.created_at.desc())
            .all()
        )

@bp.route("/<uuid:tender_id>/attachments/all")
class AllAttachments(MethodView):

    @bp.response(200, AttachmentSchema(many=True))
    def get(self, tender_id):
        """For evaluator: both the tender files and all bid files for that tender."""
        # 1) tender attachments
        tender_q = (
            Attachment.query
            .filter_by(owner_type="tender", owner_id=tender_id)
        )

        # 2) collect all bids for this tender
        bid_ids_subq = (
            db.session.query(Bid.id)
            .filter(Bid.tender_id == tender_id)
            .subquery()
        )
        bid_q = (
            Attachment.query
            .filter(
                Attachment.owner_type == "bid",
                Attachment.owner_id.in_(bid_ids_subq)
            )
        )

        # union and return
        return (
            tender_q
            .union_all(bid_q)
            .order_by(Attachment.created_at.desc())
            .all()
        )

