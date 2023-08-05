import random
import string
from datetime import datetime, timedelta

import jwt


def encode(app_key, app_secret):
    rand_str = random.choices(string.ascii_uppercase + string.digits, k=32)
    return jwt.encode(
        payload={'iss': app_key, 'iat': datetime.utcnow(), 'jti': rand_str,
                 'exp': datetime.utcnow() + timedelta(seconds=10)},
        key=app_secret,
        algorithm='HS256'
    )
