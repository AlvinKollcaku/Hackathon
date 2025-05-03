from flask import Blueprint, request, jsonify, abort
from models import TeamMember
from schemas import TeamMemberSchema
from DB import db

tm_bp = Blueprint('team_members', __name__, url_prefix='/team_members')

# Schemas
tm_schema = TeamMemberSchema()
tms_schema = TeamMemberSchema(many=True)

@tm_bp.route('', methods=['GET'])
def list_team_members():
    """List all team members"""
    tms = TeamMember.query.all()
    return jsonify(tms_schema.dump(tms)), 200

@tm_bp.route('', methods=['POST'])
def create_team_member():
    """Create a new team member"""
    data = request.get_json() or {}
    try:
        tm = tm_schema.load(data, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.add(tm)
    db.session.commit()
    return jsonify(tm_schema.dump(tm)), 201

@tm_bp.route('/<uuid:tm_id>', methods=['GET'])
