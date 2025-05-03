from flask import Blueprint, request, jsonify, abort
from models import VendorCompany
from schemas import VendorCompanySchema
from DB import db

vendor_bp = Blueprint('vendors', __name__, url_prefix='/vendors')

# Schemas
vendor_schema = VendorCompanySchema()
vendors_schema = VendorCompanySchema(many=True)

@vendor_bp.route('', methods=['GET'])
def list_vendors():
    vendors = VendorCompany.query.all()
    return jsonify(vendors_schema.dump(vendors)), 200

@vendor_bp.route('', methods=['POST'])
def create_vendor():
    data = request.get_json() or {}
    try:
        vendor = vendor_schema.load(data, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.add(vendor)
    db.session.commit()
    return jsonify(vendor_schema.dump(vendor)), 201

@vendor_bp.route('/<uuid:vendor_id>', methods=['GET'])
def get_vendor(vendor_id):
    vendor = VendorCompany.query.get_or_404(vendor_id)
    return jsonify(vendor_schema.dump(vendor)), 200

@vendor_bp.route('/<uuid:vendor_id>', methods=['PUT'])
def replace_vendor(vendor_id):
    vendor = VendorCompany.query.get_or_404(vendor_id)
    data = request.get_json() or {}
    try:
        updated = vendor_schema.load(data, instance=vendor, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(vendor_schema.dump(updated)), 200

@vendor_bp.route('/<uuid:vendor_id>', methods=['PATCH'])
def update_vendor(vendor_id):
    vendor = VendorCompany.query.get_or_404(vendor_id)
    data = request.get_json() or {}
    try:
        updated = vendor_schema.load(data, instance=vendor, session=db.session, partial=True)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(vendor_schema.dump(updated)), 200

@vendor_bp.route('/<uuid:vendor_id>', methods=['DELETE'])
def delete_vendor(vendor_id):
    vendor = VendorCompany.query.get_or_404(vendor_id)
    db.session.delete(vendor)
    db.session.commit()
    return '', 204

