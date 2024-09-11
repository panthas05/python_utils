import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import json
import time


def base64_url_encode(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii").rstrip("=")


def get_jwt(
    issuer: str,
    audience: str,
    scopes: list[str],
    private_key: str,
) -> str:
    # building header and claim set hash
    now = int(time.time())
    header = base64_url_encode(
        json.dumps({"alg": "RS256", "typ": "JWT"}).encode("ascii")
    )
    claim_set = base64_url_encode(
        json.dumps(
            {
                "iss": issuer,
                "scope": " ".join(scopes),
                "aud": audience,
                "exp": now + 1,
                "iat": now,
            }
        ).encode("ascii")
    )
    hash_input = f"{header}.{claim_set}"
    # building signature hash
    private_key_instance = serialization.load_pem_private_key(
        private_key.encode(),
        password=None,
    )
    if not isinstance(private_key_instance, rsa.RSAPrivateKey):
        raise Exception(f"Please add handling for {type(private_key_instance)}")
    signature = private_key_instance.sign(
        hash_input.encode("ascii"),
        padding.PKCS1v15(),
        hashes.SHA256(),
    )
    encoded_signature = base64_url_encode(signature)
    return f"{hash_input}.{encoded_signature}"
