from flask import Blueprint, request, jsonify, abort
from models import User
from schemas import PlainUserSchema
from DB import db

import requests, os
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    get_jwt_identity, jwt_required, get_jwt
)
from flask import jsonify
from datetime import datetime
from blocklist import BLOCKLIST

user_bp = Blueprint('users', __name__, url_prefix='/users')

# Login schema now only requires email and password
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

def admin_required():
    claims = get_jwt()
    if claims.get("role") != "admin":
        abort(403, message="Admin privileges required.")

def proc_officer_required():
    claims = get_jwt()
    if claims.get("role") != "proc_officer":
        abort(403, message="Procurement Officer privileges required.")

def evaluator_required():
    claims = get_jwt()
    if claims.get("role") != "evaluator":
        abort(403, message="Evaluator privileges required.")

def vendor_required():
    claims = get_jwt()
    if claims.get("role") != "vendor":
        abort(403, message="Vendor privileges required.")

def get_identity(user):
    return user.id

@user_bp.route("/login")
class UserLogin(MethodView):

    @user_bp.arguments(LoginSchema)
    def post(self, user_data):
        email    = user_data["email"]
        password = user_data["password"]

        # single-table lookup
        user = User.query.filter_by(email=email).first()
        if not user or not pbkdf2_sha256.verify(password, user.password_hash):
            abort(401, message="Invalid credentials.")

        # (Optional) track last‐login if you add that column:
        # user.last_login = datetime.utcnow()
        # db.session.commit()

        identity          = get_identity(user)
        additional_claims = {"role": user.role}
        access_token      = create_access_token(
                                identity=identity,
                                additional_claims=additional_claims,
                                fresh=True
                             )

        return {"access_token": access_token}, 200

@user_bp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

