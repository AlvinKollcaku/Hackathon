import os
import tempfile
import traceback
from flask import request, jsonify
from flask_smorest import Blueprint
from utils.pdf_extractor import extract_table_from_pdf
from ai_evaluator import evaluate_documents

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/evaluate-docs', methods=['POST'])
def evaluate_docs():
    try:
        # debug what arrived
        print(">>> request.files keys:", list(request.files.keys()))

        req_file = request.files.get('requirements')
        bid_file = request.files.get('bid')
        if not req_file or not bid_file:
            return jsonify({"error": "Both 'requirements' and 'bid' files are required"}), 400

        # save to temp PDFs
        temp_req = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_req.write(req_file.read()); temp_req.flush()
        temp_bid = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_bid.write(bid_file.read()); temp_bid.flush()

        print(f">>> Saved to {temp_req.name}, {temp_bid.name}")

        # extract with stream mode
        req_df = extract_table_from_pdf(temp_req.name, pages="1-end", flavor="stream")
        bid_df = extract_table_from_pdf(temp_bid.name, pages="1-end", flavor="stream")

        # call the LLM-based evaluator
        result = evaluate_documents(req_df, bid_df)
        print(">>> Evaluation result:", result)

        return jsonify(result), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

    finally:
        # cleanup temps
        for f in (temp_req, temp_bid):
            try: os.unlink(f.name)
            except: pass
