import hashlib
from my_db import Session, User
from sqlalchemy import exists
import re

# Create an api key from email and username for each user
def generate_api_key(email: str, username: str) -> str:
    mystring = email + username
    hash_object = hashlib.sha256(mystring.encode())
    return hash_object.hexdigest()

# Check if an api key is valid and return the corresponding user
def check_api_key(api_key: str) -> User:
    if not isinstance(api_key, str) or not api_key or not re.match(r'^[0-9a-f]{64}$', api_key):
        return None
    with Session() as session:
        print('I was here')
        if session.query(exists().where(User.api_key == api_key)).scalar():
            return session.query(User).filter_by(api_key=api_key).one()
    return None

# Hash a password using SHA-256 algorithm
def hash_password(password: str) -> str:
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()

