from flask import Blueprint, request, jsonify, abort
from models import Tender
from schemas import TenderSchema
from DB import db

TenderSchema(strict=True)

tender_bp = Blueprint('tenders', __name__, url_prefix='/tenders')

# Schemas
tender_schema = TenderSchema()
tenders_schema = TenderSchema(many=True)

@tender_bp.route('', methods=['GET'])
def list_tenders():
    tenders = Tender.query.order_by(Tender.created_at.desc()).all()
    return jsonify(tenders_schema.dump(tenders)), 200

@tender_bp.route('', methods=['POST'])
def create_tender():
    data = request.get_json() or {}
    try:
        tender = tender_schema.load(data, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.add(tender)
    db.session.commit()
    return jsonify(tender_schema.dump(tender)), 201

@tender_bp.route('/<uuid:tender_id>', methods=['GET'])
def get_tender(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    return jsonify(tender_schema.dump(tender)), 200

@tender_bp.route('/<uuid:tender_id>', methods=['PUT'])
def replace_tender(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    data = request.get_json() or {}
    try:
        updated = tender_schema.load(data, instance=tender, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(tender_schema.dump(updated)), 200

@tender_bp.route('/<uuid:tender_id>', methods=['PATCH'])
def update_tender(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    data = request.get_json() or {}
    try:
        updated = tender_schema.load(data, instance=tender, session=db.session, partial=True)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(tender_schema.dump(updated)), 200

@tender_bp.route('/<uuid:tender_id>', methods=['DELETE'])
def delete_tender(tender_id):
    tender = Tender.query.get_or_404(tender_id)
    db.session.delete(tender)
    db.session.commit()
    return '', 204
