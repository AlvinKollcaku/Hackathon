from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from DB import db
from models import Bid
from schemas import PlainBidSchema, BidSchema

bp = Blueprint('bids', __name__, url_prefix='/bids')

@bp.route('')
class BidList(MethodView):
    @jwt_required()
    @bp.response(200, BidSchema(many=True))
    def get(self):
        """List all bids"""
        return Bid.query.all()

    @jwt_required()
    @bp.arguments(PlainBidSchema)
    @bp.response(201, BidSchema)
    def post(self, bid_data):
        """Create a new bid"""
        bid = Bid(**bid_data)
        db.session.add(bid)
        db.session.commit()
        return bid

@bp.route('/<uuid:bid_id>')
class BidResource(MethodView):
    @jwt_required()
    @bp.response(200, BidSchema)
    def get(self, bid_id):
        """Fetch a bid by ID"""
        return Bid.query.get_or_404(bid_id)

    @jwt_required()
    @bp.arguments(PlainBidSchema)
    @bp.response(200, BidSchema)
    def put(self, bid_data, bid_id):
        """Replace an existing bid entirely"""
        bid = Bid.query.get_or_404(bid_id)
        #bid = BidSchema().load(bid_data, instance=bid, session=db.session)
        db.session.commit()
        return bid

    @jwt_required()
    @bp.arguments(PlainBidSchema, partial=True)
    @bp.response(200, BidSchema)
    def patch(self, bid_data, bid_id):
        """Partially update a bid"""
        bid = Bid.query.get_or_404(bid_id)
        #bid = BidSchema().load(bid_data, instance=bid, session=db.session, partial=True)
        db.session.commit()
        return bid

    @jwt_required()
    def delete(self, bid_id):
        """Delete a bid"""
        bid = Bid.query.get_or_404(bid_id)
        db.session.delete(bid)
        db.session.commit()
        return '', 204
