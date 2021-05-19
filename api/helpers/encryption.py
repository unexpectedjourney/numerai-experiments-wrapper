import hashlib
from datetime import datetime

import jwt

JWT_ALGORITHM = 'HS256'
JWT_SECRET = 'secret'


def encrypt_password(hash_string):
    sha_signature = hashlib.md5(hash_string.encode()).hexdigest()
    return sha_signature


def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'created': datetime.now().__str__()
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return jwt_token.decode("utf-8")
