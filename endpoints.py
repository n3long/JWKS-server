from flask import jsonify, request
from datetime import datetime, timedelta
import jwt
from key_manager import get_public_key_jwks, get_private_key, get_kid

def register_endpoints(app):
    @app.route('/.well-known/jwks.json', methods=['GET'])
    def jwks():
        return jsonify(get_public_key_jwks())

    @app.route('/auth', methods=['POST'])
    def auth():
        expired = request.args.get('expired', 'false').lower() == 'true'
        if expired:
            exp = datetime.utcnow() - timedelta(days=1)  # Expired token
        else:
            exp = datetime.utcnow() + timedelta(minutes=15)  # 15 minutes expiry

        payload = {
            "sub": "fake_user",
            "exp": exp
        }

        token = jwt.encode(payload, get_private_key(), algorithm='RS256', headers={"kid": get_kid()})

        return jsonify({"access_token": token})