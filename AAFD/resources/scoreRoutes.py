from flask import Blueprint, request, jsonify, abort
from models import Score
from schemas import ScoreSchema
from DB import db

score_bp = Blueprint('scores', __name__, url_prefix='/scores')

# Schemas
score_schema = ScoreSchema()
scores_schema = ScoreSchema(many=True)

@score_bp.route('', methods=['GET'])
def list_scores():
    scores = Score.query.all()
    return jsonify(scores_schema.dump(scores)), 200

@score_bp.route('', methods=['POST'])
def create_score():
    data = request.get_json() or {}
    try:
        score = score_schema.load(data, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.add(score)
    db.session.commit()
    return jsonify(score_schema.dump(score)), 201

@score_bp.route('/<uuid:score_id>', methods=['GET'])
def get_score(score_id):
    score = Score.query.get_or_404(score_id)
    return jsonify(score_schema.dump(score)), 200

@score_bp.route('/<uuid:score_id>', methods=['PUT'])
def replace_score(score_id):
    score = Score.query.get_or_404(score_id)
    data = request.get_json() or {}
    try:
        updated = score_schema.load(data, instance=score, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(score_schema.dump(updated)), 200

@score_bp.route('/<uuid:score_id>', methods=['PATCH'])
def update_score(score_id):
    score = Score.query.get_or_404(score_id)
    data = request.get_json() or {}
    try:
        updated = score_schema.load(data, instance=score, session=db.session, partial=True)
    except Exception as e:
        abort(400, str(e))
    db.session.commit()
    return jsonify(score_schema.dump(updated)), 200

@score_bp.route('/<uuid:score_id>', methods=['DELETE'])
def delete_score(score_id):
    score = Score.query.get_or_404(score_id)
    db.session.delete(score)
    db.session.commit()
    return '', 204
