from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

# Generate an RSA key pair
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key

private_key = generate_key_pair()
public_key = private_key.public_key()
kid = "1"
expiry = datetime.utcnow() + timedelta(days=1)  # 1 day expiry

# Get the private key in PEM format
def get_private_key():
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

# Get the JWKS representation of the public key
def get_public_key_jwks():
    if datetime.utcnow() < expiry:
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        # Conversion to JWKS format
        jwks = {
            "keys": [
                {
                    "kty": "RSA",
                    "use": "sig",
                    "kid": kid,
                    "n": "MODULUS",
                    "e": "EXPONENT"
                }
            ]
        }
        return jwks
    else:
        return {"keys": []}

# Get the Key ID
def get_kid():
    return kid