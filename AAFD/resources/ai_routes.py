# routes/ai_routes.py
import os
import tempfile
from flask import Blueprint, request, jsonify

from utils.pdf_extractor import extract_table_from_pdf
from ai_evaluator import evaluate_documents

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/evaluate-docs', methods=['POST'])
def evaluate_docs():
    """
    Expects a multipart/form-data POST with two files:
      • 'requirements' → the requirements-template PDF
      • 'bid'          → the vendor’s bid PDF
    Returns JSON with report, summary, scores, total_score.
    """
    req_file = request.files.get('requirements')
    bid_file = request.files.get('bid')
    if not req_file or not bid_file:
        return jsonify({"error":"Both 'requirements' and 'bid' files are required"}), 400

    # save to temp files
    temp_req = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_req.write(req_file.read());  temp_req.flush()

    temp_bid = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_bid.write(bid_file.read());  temp_bid.flush()

    # extract tables
    req_df = extract_table_from_pdf(temp_req.name, pages="1-end", engine="camelot")
    bid_df = extract_table_from_pdf(temp_bid.name, pages="1-end", engine="camelot")

    # call the evaluator
    result = evaluate_documents(req_df, bid_df)

    # cleanup
    try:
        os.unlink(temp_req.name)
        os.unlink(temp_bid.name)
    except OSError:
        pass

    return jsonify(result), 200
