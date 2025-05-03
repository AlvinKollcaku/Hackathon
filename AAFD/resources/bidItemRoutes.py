from flask import Blueprint, request, jsonify, abort
from models import BidItem
from schemas import BidItemSchema
from DB import db

bid_item_bp = Blueprint('bid_items', __name__, url_prefix='/bid_items')

# Schemas
bid_item_schema = BidItemSchema()
bid_items_schema = BidItemSchema(many=True)

@bid_item_bp.route('', methods=['GET'])
def list_bid_items():
    items = BidItem.query.all()
    return jsonify(bid_items_schema.dump(items)), 200

@bid_item_bp.route('', methods=['POST'])
def create_bid_item():
    data = request.get_json() or {}
    try:
        item = bid_item_schema.load(data, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.add(item)
    db.session.commit()
    return jsonify(bid_item_schema.dump(item)), 201

@bid_item_bp.route('/<uuid:item_id>', methods=['GET'])
def get_bid_item(item_id):
    item = BidItem.query.get_or_404(item_id)
    return jsonify(bid_item_schema.dump(item)), 200

@bid_item_bp.route('/<uuid:item_id>', methods=['PUT'])
def replace_bid_item(item_id):
    item = BidItem.query.get_or_404(item_id)
    data = request.get_json() or {}
    try:
        updated = bid_item_schema.load(data, instance=item, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(bid_item_schema.dump(updated)), 200

@bid_item_bp.route('/<uuid:item_id>', methods=['PATCH'])
def update_bid_item(item_id):
    item = BidItem.query.get_or_404(item_id)
    data = request.get_json() or {}
    try:
        updated = bid_item_schema.load(data, instance=item, session=db.session, partial=True)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(bid_item_schema.dump(updated)), 200

@bid_item_bp.route('/<uuid:item_id>', methods=['DELETE'])
def delete_bid_item(item_id):
    item = BidItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return '', 204