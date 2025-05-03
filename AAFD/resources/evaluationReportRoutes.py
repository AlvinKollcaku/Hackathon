from flask import Blueprint, request, jsonify, abort
from models import EvaluationReport
from schemas import EvaluationReportSchema
from DB import db

eval_report_bp = Blueprint('evaluation_reports', __name__, url_prefix='/evaluation_reports')

# Schemas
eval_report_schema = EvaluationReportSchema()
eval_reports_schema = EvaluationReportSchema(many=True)

@eval_report_bp.route('', methods=['GET'])
def list_reports():
    reports = EvaluationReport.query.all()
    return jsonify(eval_reports_schema.dump(reports)), 200

@eval_report_bp.route('', methods=['POST'])
def create_report():
    data = request.get_json() or {}
    try:
        report = eval_report_schema.load(data, session=db.session)
    except Exception as e:
        abort(400, str(e))
    db.session.add(report)
    db.session.commit()
    return jsonify(eval_report_schema.dump(report)), 201

@eval_report_bp.route('/<uuid:report_id>', methods=['GET'])
def get_report(report_id):
    report = EvaluationReport.query.get_or_404(report_id)
    return jsonify(eval_report_schema.dump(report)), 200

