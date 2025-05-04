from flask import request, abort, current_app
from flask.views import MethodView
from flask_smorest import Blueprint

from DB      import db
from models  import Bid, Attachment
from schemas import AttachmentSchema
from google_drive import upload_file_to_drive  # <— import it

bp = Blueprint('bids', __name__, url_prefix='/tenders')

@bp.route('/<uuid:tender_id>/bids/<uuid:bid_id>/attachments', methods=['POST'])
class BidUpload(MethodView):

    @bp.response(201, AttachmentSchema)
    def post(self, tender_id, bid_id):
        file = request.files.get('file')
        if not file:
            abort(400, "No file provided")

        # optional: validate the bid → tender relationship
        bid = Bid.query.get_or_404(bid_id)
        if str(bid.tender_id) != str(tender_id):
            abort(400, "Bid does not belong to this tender")

        try:
            # pass the Werkzeug FileStorage’s stream, filename & mimetype
            public_url = upload_file_to_drive(
                file.stream,
                file.filename,
                file.mimetype
            )
        except Exception as e:
            current_app.logger.exception("Drive upload failed")
            abort(502, "Drive upload error: " + str(e))

        # save the attachment record
        attach = Attachment(
            owner_type='bid',
            owner_id=bid_id,
            file_name=file.filename,
            file_url=public_url
        )
        db.session.add(attach)
        db.session.commit()

        return attach
