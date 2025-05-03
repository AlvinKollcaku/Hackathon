from flask import Blueprint, request, jsonify, abort
from models import Bid
from schemas import BidSchema
from DB import db

bid_bp = Blueprint('bids', __name__, url_prefix='/bids')

# Schemas
bid_schema = BidSchema()
bids_schema = BidSchema(many=True)

@bid_bp.route('', methods=['GET'])
def list_bids():
    """List all bids"""
    bids = Bid.query.all()
    return jsonify(bids_schema.dump(bids)), 200

@bid_bp.route('', methods=['POST'])
def create_bid():
    """Create a new bid"""
    data = request.get_json() or {}
    try:
        bid = bid_schema.load(data, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.add(bid)
    db.session.commit()
    return jsonify(bid_schema.dump(bid)), 201

@bid_bp.route('/<uuid:bid_id>', methods=['GET'])
def get_bid(bid_id):
    """Fetch a bid by ID"""
    bid = Bid.query.get_or_404(bid_id)
    return jsonify(bid_schema.dump(bid)), 200

@bid_bp.route('/<uuid:bid_id>', methods=['PUT'])
def replace_bid(bid_id):
    """Replace an existing bid entirely"""
    bid = Bid.query.get_or_404(bid_id)
    data = request.get_json() or {}
    try:
        updated = bid_schema.load(data, instance=bid, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(bid_schema.dump(updated)), 200

@bid_bp.route('/<uuid:bid_id>', methods=['PATCH'])
def update_bid(bid_id):
    """Partially update a bid"""
    bid = Bid.query.get_or_404(bid_id)
    data = request.get_json() or {}
    try:
        updated = bid_schema.load(data, instance=bid, session=db.session, partial=True)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(bid_schema.dump(updated)), 200

@bid_bp.route('/<uuid:bid_id>', methods=['DELETE'])
def delete_bid(bid_id):
    """Delete a bid"""
    bid = Bid.query.get_or_404(bid_id)
    db.session.delete(bid)
    db.session.commit()
    return '', 204
