from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from passlib.hash import pbkdf2_sha256

plaintext_password = "vendor"
hashed_password = pbkdf2_sha256.hash(plaintext_password)
print(hashed_password)

