from unittest import TestCase

from src import jwt

import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa


class GetJwtTests(TestCase):
    service_account_email = "foo@bar.com"

    def test_generates_valid_signature(self):
        # set up
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        pem_representation = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()
        # the test itself
        token = jwt.get_jwt(
            "foo@bar.com",
            "https://www.foobar.com",
            ["https://www.foobar.com/auth"],
            pem_representation,
        )
        hash_input, signature_str = token.rsplit(".", maxsplit=1)
        # verifying signature
        signature = base64.b64decode((signature_str + "==").encode("ascii"))
        public_key = private_key.public_key()
        public_key.verify(
            signature, hash_input.encode("ascii"), padding.PKCS1v15(), hashes.SHA256()
        )
