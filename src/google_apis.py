from django.core.cache import cache

from src import jwt

import requests


def get_access_token(
    issuer: str,
    scopes: list[str],
    private_key: str,
    cache_key: str,
) -> str:
    access_token: str = cache.get(cache_key) or ""
    if not access_token:
        token = jwt.get_jwt(
            issuer,
            "https://oauth2.googleapis.com/token",
            scopes,
            private_key,
        )

        response = requests.post(
            "https://oauth2.googleapis.com/token",
            {
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": token,
            },
            timeout=300,
        )
        response_json = response.json()

        access_token = response_json["access_token"]
        timeout = (response_json.get("expires_in") or 3600) - 10
        cache.set(cache_key, access_token, timeout=timeout)

    return access_token
