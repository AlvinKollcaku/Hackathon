from sqlalchemy.dialects.postgresql import ENUM

user_role_enum = ENUM('admin','proc_officer','evaluator','vendor', name='user_role', create_type=False)
tender_status_enum = ENUM('draft','published','closed','evaluation','awarded','archived', name='tender_status', create_type=False)
criterion_type_enum = ENUM('price','technical','administrative', name='criterion_type', create_type=False)
bid_status_enum = ENUM('submitted','withdrawn','invalid','evaluated','winning','lost', name='bid_status', create_type=False)