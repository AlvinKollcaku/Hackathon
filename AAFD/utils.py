from flask_jwt_extended import get_jwt
from flask_smorest import abort

def admin_required():
    claims = get_jwt()
    if claims.get("role") != "admin":
        abort(403, message="Admin privileges required.")

def proc_officer_required():
    claims = get_jwt()
    if claims.get("role") != "proc_officer":
        abort(403, message="Procurement Officer privileges required.")

def proc_officer_or_vendor_required():
    claims = get_jwt()
    if claims.get("role") != "proc_officer" and claims.get("role") != "vendor":
        abort(403, message="Procurement Officer or vendor privileges required.")

def evaluator_required():
    claims = get_jwt()
    if claims.get("role") != "evaluator":
        abort(403, message="Evaluator privileges required.")

def vendor_required():
    claims = get_jwt()
    if claims.get("role") != "vendor":
        abort(403, message="Vendor privileges required.")