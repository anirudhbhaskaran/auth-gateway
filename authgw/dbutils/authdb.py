import datetime
import os
import random
import sqlite3
import string
from urllib.parse import quote_plus


def generate_random_string(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))


class AuthDb:

    # DB Structure - AUTHY
    # id - Primary ID Key
    # clientId - Client ID
    # clientKey - Client Key
    # clientSecret - Client Secret

    # DB Structure - TOKENS
    # id - Primary ID Key
    # clientId - Client ID
    # token - Refresh Token
    # validUntil - Token Validity

    con = None
    def __init__(self):
        pass

    @staticmethod
    def _get_con():
        if not AuthDb.con:
            AuthDb.con = sqlite3.connect(os.environ.get("AUTH_DB_LOCATION", "authserver.db"))
        return AuthDb.con
    
    def _get_client_details(self, client_id):
        cur = self._get_con().cursor()
        res = cur.execute("SELECT * FROM {} WHERE clientId='{}';".format(os.environ.get("AUTH_DB_TABLE", "AUTHY"), quote_plus(client_id)))
        return res.fetchone()


    def _validate_client_token(self, client_id, token):
        cur = self._get_con().cursor()
        res = cur.execute("SELECT * FROM {} WHERE clientId='{}' AND token='{}' AND validUntil >= '{}';".format(os.environ.get("AUTH_DB_TOKEN_TABLE", "TOKENS"), quote_plus(client_id), quote_plus(token), quote_plus(datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ"))))
        return res.fetchone()
    
    def _insert_new_token(self, client_id):
        token = generate_random_string(128)
        validity = (datetime.datetime.now() + datetime.timedelta(minutes=int(os.environ.get("TOKEN_EXPIRY", 60)))).strftime("%Y-%m-%dT%H-%M-%SZ")
        cur = self._get_con().cursor()
        cur.execute("INSERT INTO {} (clientId, token, validUntil) VALUES('{}', '{}', '{}');".format(os.environ.get("AUTH_DB_TOKEN_TABLE", "TOKENS"), quote_plus(client_id), quote_plus(token), quote_plus(validity)))
        self._get_con().commit()
        return {
            "token": token,
            "validUntil": validity
        }

    @staticmethod
    def _close_con():
        if AuthDb.con:
            AuthDb.con.close()
        AuthDb.con = None
