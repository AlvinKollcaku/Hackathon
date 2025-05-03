from flask import Blueprint, request, jsonify, abort
from models import Criterion
from schemas import CriterionSchema
from DB import db

criteria_bp = Blueprint('criteria', __name__, url_prefix='/criteria')

# Schemas
criterion_schema = CriterionSchema()
criteria_schema = CriterionSchema(many=True)

@criteria_bp.route('', methods=['GET'])
def list_criteria():
    crits = Criterion.query.all()
    return jsonify(criteria_schema.dump(crits)), 200

@criteria_bp.route('', methods=['POST'])
def create_criterion():
    data = request.get_json() or {}
    try:
        crit = criterion_schema.load(data, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.add(crit)
    db.session.commit()
    return jsonify(criterion_schema.dump(crit)), 201

@criteria_bp.route('/<uuid:crit_id>', methods=['GET'])
def get_criterion(crit_id):
    crit = Criterion.query.get_or_404(crit_id)
    return jsonify(criterion_schema.dump(crit)), 200

@criteria_bp.route('/<uuid:crit_id>', methods=['PUT'])
def replace_criterion(crit_id):
    crit = Criterion.query.get_or_404(crit_id)
    data = request.get_json() or {}
    try:
        updated = criterion_schema.load(data, instance=crit, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(criterion_schema.dump(updated)), 200

@criteria_bp.route('/<uuid:crit_id>', methods=['PATCH'])
def update_criterion(crit_id):
    crit = Criterion.query.get_or_404(crit_id)
    data = request.get_json() or {}
    try:
        updated = criterion_schema.load(data, instance=crit, session=db.session, partial=True)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(criterion_schema.dump(updated)), 200

@criteria_bp.route('/<uuid:crit_id>', methods=['DELETE'])

def delete_criterion(crit_id):
    crit = Criterion.query.get_or_404(crit_id)
    db.session.delete(crit)
    db.session.commit()
    return '', 204