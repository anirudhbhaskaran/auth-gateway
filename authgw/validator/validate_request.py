import datetime
import functools
import jwt

from fastapi import status

from authgw.dbutils import authdb


def _validate_token_request(auth):
    try:
        token = str(auth).replace("JWT ", "")
        payload = jwt.decode(token, options={"verify_signature": False})
        client_id = payload["clientId"]
        client_key = payload["clientKey"]

        db_obj = authdb.AuthDb()
        
        client_details = db_obj._get_client_details(client_id=client_id)
        if not client_details:
            return False, status.HTTP_403_FORBIDDEN, "Non-existent Client"
        
        if client_details[2] != client_key:
            return False, status.HTTP_401_UNAUTHORIZED, "Invalid Client Credentials"
        # Check if request is signed
        _ = jwt.decode(token, client_details[3], algorithms=["HS256"])
        token_details = db_obj._insert_new_token(client_id=client_id)
        
        db_obj._close_con()
        return True, status.HTTP_200_OK, token_details
    except:
        return False, status.HTTP_403_FORBIDDEN, "Invalid Request"


def _validate_request(*args, **kwargs):
    try:
        authorization = kwargs.get("authorization", None)
        if not authorization:
            return False
        token = str(authorization).replace("JWT ", "")
        payload = jwt.decode(token, options={"verify_signature": False})
        client_id = payload["clientId"]
        # Check if refresh token is valid
        refresh_token = payload["token"]

        db_obj = authdb.AuthDb()

        validation = db_obj._validate_client_token(client_id=client_id, token=refresh_token)
        if not validation:
            return False
        
        client_details = db_obj._get_client_details(client_id=client_id)
        if not client_details:
            return False
        
        db_obj._close_con()
        
        # Check if request is signed
        _ = jwt.decode(token, client_details[3], algorithms=["HS256"])
        return True
    except:
        return False


def validate(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        validation = _validate_request(*args, **kwargs)
        if validation:
            return func(*args, **kwargs)
        else:
            kwargs.get("response").status_code = status.HTTP_401_UNAUTHORIZED
            return "UNAUTHORIZED"
    return wrapper
