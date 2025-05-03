from flask import Blueprint, request, jsonify, abort
from models import VendorContract
from schemas import VendorContractSchema
from DB import db

vc_bp = Blueprint('vendor_contracts', __name__, url_prefix='/vendor_contracts')

# Schemas
vc_schema = VendorContractSchema()
vcs_schema = VendorContractSchema(many=True)

@vc_bp.route('', methods=['GET'])
def list_vendor_contracts():
    """List all vendor contracts"""
    vcs = VendorContract.query.all()
    return jsonify(vcs_schema.dump(vcs)), 200

@vc_bp.route('', methods=['POST'])
def create_vendor_contract():
    """Create a new vendor contract"""
    data = request.get_json() or {}
    try:
        vc = vc_schema.load(data, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.add(vc)
    db.session.commit()
    return jsonify(vc_schema.dump(vc)), 201

@vc_bp.route('/<uuid:vc_id>', methods=['GET'])
def get_vendor_contract(vc_id):
    """Fetch a vendor contract by ID"""
    vc = VendorContract.query.get_or_404(vc_id)
    return jsonify(vc_schema.dump(vc)), 200

@vc_bp.route('/<uuid:vc_id>', methods=['PUT'])
def replace_vendor_contract(vc_id):
    """Replace an existing vendor contract entirely"""
    vc = VendorContract.query.get_or_404(vc_id)
    data = request.get_json() or {}
    try:
        updated = vc_schema.load(data, instance=vc, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(vc_schema.dump(updated)), 200

@vc_bp.route('/<uuid:vc_id>', methods=['PATCH'])
def update_vendor_contract(vc_id):
    """Partially update a vendor contract"""
    vc = VendorContract.query.get_or_404(vc_id)
    data = request.get_json() or {}
    try:
        updated = vc_schema.load(data, instance=vc, session=db.session, partial=True)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(vc_schema.dump(updated)), 200

@vc_bp.route('/<uuid:vc_id>', methods=['DELETE'])
def delete_vendor_contract(vc_id):
    """Delete a vendor contract"""
    vc = VendorContract.query.get_or_404(vc_id)
    db.session.delete(vc)
    db.session.commit()
    return '', 204
