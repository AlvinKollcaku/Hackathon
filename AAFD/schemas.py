from marshmallow import Schema, fields, validate
from enums import *

class PlainTenderSchema(Schema):
    id            = fields.UUID(dump_only=True)
    code          = fields.Str()
    title         = fields.Str(required=True)
    description   = fields.Str()
    publish_at    = fields.DateTime()
    deadline      = fields.DateTime()
    budget  = fields.Decimal(as_string=True)
    status = fields.Str(
        validate=validate.OneOf(tender_status_enum.enums)  # Access the enum values through the 'enums' property
    )
    created_by    = fields.UUID(dump_only=True)
    created_at    = fields.DateTime(dump_only=True)

class PlainVendorCompanySchema(Schema):
    id          = fields.UUID(dump_only=True)
    legal_name  = fields.Str(required=True)
    vat_number  = fields.Str()
    country     = fields.Str()
    created_at  = fields.DateTime(dump_only=True)

class PlainUserSchema(Schema):
    # PK + basics
    id          = fields.UUID(dump_only=True)
    full_name   = fields.Str(required=True)
    email       = fields.Email(required=True)

    # Accept plaintext password on input, never expose hash on output
    password    = fields.Str(
        required=True,
        load_only=True,
        attribute="password_hash"
    )

    # Enum stored in DB → validate against enum values
    role = fields.Str(
        required=True,
        validate=validate.OneOf(user_role_enum.enums)
    )

    created_at  = fields.DateTime(dump_only=True)
    is_active   = fields.Bool(dump_only=True)

    # FK to vendor company (if applicable)
    vendor_id   = fields.UUID(load_only=True)

class PlainCriterionSchema(Schema):
    id          = fields.UUID(dump_only=True)
    tender_id   = fields.UUID(required=True, load_only=True)
    name        = fields.Str(required=True)
    type        = fields.Str(
        required=True,
        validate=validate.OneOf(criterion_type_enum.enums)
    )
    weight_pct  = fields.Decimal(as_string=True, required=True)
    mandatory   = fields.Bool(required=True)
    max_score   = fields.Int(required=True)
    position    = fields.Int(required=True)

class PlainBidItemSchema(Schema):
    id            = fields.UUID(dump_only=True)
    bid_id        = fields.UUID(required=True, load_only=True)
    criterion_id  = fields.UUID(required=True, load_only=True)
    value_text    = fields.Str()
    value_numeric = fields.Decimal(as_string=True)
    file_url      = fields.Str()

class PlainBidSchema(Schema):
    id                = fields.UUID(dump_only=True)
    tender_id         = fields.UUID(required=True, load_only=True)
    vendor_id         = fields.UUID(required=True, load_only=True)
    submission_date      = fields.DateTime(dump_only=True)
    status            = fields.Str(
                          validate=validate.OneOf(bid_status_enum.enums),
                          required=True
                       )
    amount       = fields.Decimal(as_string=True)
    total_ai_score    = fields.Decimal(as_string=True)
    total_final_score = fields.Decimal(as_string=True)

class PlainScoreSchema(Schema):
    id             = fields.UUID(dump_only=True)
    bid_id         = fields.UUID(required=True, load_only=True)
    criterion_id   = fields.UUID(required=True, load_only=True)
    evaluator_id   = fields.UUID(required=True, load_only=True)
    ai_suggested   = fields.Decimal(as_string=True)
    evaluator_score = fields.Decimal(as_string=True)
    final_score    = fields.Decimal(as_string=True)
    comment        = fields.Str()

class PlainEvaluationReportSchema(Schema):
    id          = fields.UUID(dump_only=True)
    tender_id   = fields.UUID(required=True, load_only=True)
    pdf_url     = fields.Str(required=True)
    approved_by = fields.UUID(load_only=True)
    created_at  = fields.DateTime(dump_only=True)
    signed_at   = fields.DateTime(dump_only=True)

class PlainTeamMemberSchema(Schema):
    id               = fields.UUID(dump_only=True)
    bid_id           = fields.UUID(required=True, load_only=True)
    full_name        = fields.Str(required=True)
    birth_year       = fields.Int()
    education        = fields.Str()
    task_assigned    = fields.Str()
    license_info     = fields.Str()
    years_experience = fields.Int()
    cv_url           = fields.Str()

class PlainVendorContractSchema(Schema):
    id               = fields.UUID(dump_only=True)
    bid_id           = fields.UUID(required=True, load_only=True)
    contract_title   = fields.Str(required=True)
    role             = fields.Str()
    value_usd        = fields.Decimal(as_string=True)
    investor_name    = fields.Str()
    contact_details  = fields.Str()
    start_date       = fields.Date()
    completion_date  = fields.Date()
    description      = fields.Str()

class UserSchema(PlainUserSchema):
    vendor                    = fields.Nested(PlainVendorCompanySchema, dump_only=True)
    tenders_created           = fields.List(fields.Nested(PlainTenderSchema), dump_only=True)
    scores                    = fields.List(fields.Nested(PlainScoreSchema), dump_only=True)
    evaluation_reports_signed = fields.List(
        fields.Nested(PlainEvaluationReportSchema),
        dump_only=True
    )

class VendorCompanySchema(PlainVendorCompanySchema):

    users = fields.List(fields.Nested(PlainUserSchema), dump_only=True)
    bids  = fields.List(fields.Nested(PlainBidSchema),  dump_only=True)

# -----------------------------
# Basic / “plain” schema
# -----------------------------



# -----------------------------
# Full schema with relations
# -----------------------------
class TenderSchema(PlainTenderSchema):
    creator           = fields.Nested(PlainUserSchema,       dump_only=True)
    criteria          = fields.List(fields.Nested(PlainCriterionSchema), dump_only=True)
    bids              = fields.List(fields.Nested(PlainBidSchema),       dump_only=True)
    evaluation_report = fields.Nested(PlainEvaluationReportSchema,        dump_only=True)

# -----------------------------
# Basic / “plain” schema
# -----------------------------



# -----------------------------
# Full schema with relations
# -----------------------------

class BidSchema(PlainBidSchema):
    tender           = fields.Nested(PlainTenderSchema,        dump_only=True)
    vendor           = fields.Nested(PlainVendorCompanySchema, dump_only=True)
    bid_items        = fields.List(fields.Nested(PlainBidItemSchema),      dump_only=True)
    scores           = fields.List(fields.Nested(PlainScoreSchema),        dump_only=True)
    team_members     = fields.List(fields.Nested(PlainTeamMemberSchema),   dump_only=True)
    vendor_contracts = fields.List(fields.Nested(PlainVendorContractSchema), dump_only=True)

class ScoreSchema(PlainScoreSchema):
    # assumes PlainBidSchema, PlainCriterionSchema, PlainUserSchema are defined earlier
    bid        = fields.Nested(PlainBidSchema,      dump_only=True)
    criterion  = fields.Nested(PlainCriterionSchema, dump_only=True)
    evaluator  = fields.Nested(PlainUserSchema,     dump_only=True)

class EvaluationReportSchema(PlainEvaluationReportSchema):
    # assumes PlainTenderSchema and PlainUserSchema are defined earlier in schemas.py
    tender   = fields.Nested(PlainTenderSchema, dump_only=True)
    approver = fields.Nested(PlainUserSchema, dump_only=True)

class TeamMemberSchema(PlainTeamMemberSchema):
    # assumes PlainBidSchema is defined earlier in schemas.py
    bid = fields.Nested(PlainBidSchema, dump_only=True)

class VendorContractSchema(PlainVendorContractSchema):
    # assumes PlainBidSchema is defined earlier in schemas.py
    bid = fields.Nested(PlainBidSchema, dump_only=True)

class PlainAuditLogSchema(Schema):
    id          = fields.Integer(dump_only=True)
    actor_id    = fields.UUID(load_only=True)
    action      = fields.Str(required=True)
    entity_type = fields.Str(required=True)
    entity_id   = fields.UUID()
    ts          = fields.DateTime(dump_only=True)
    diff        = fields.Dict()


class AuditLogSchema(PlainAuditLogSchema):
    # If you later add a relationship `actor = db.relationship('User')` in your model,
    # you can include the nested user like so:
    # actor = fields.Nested(PlainUserSchema, dump_only=True)
    pass

class PlainAttachmentSchema(Schema):
    id         = fields.UUID(dump_only=True)
    owner_type = fields.Str(required=True)
    owner_id   = fields.UUID(required=True)
    file_name  = fields.Str(required=True)
    file_url   = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

class AttachmentSchema(PlainAttachmentSchema):
    # No additional nested relations; inherits everything from PlainAttachmentSchema
    pass