from django.core.cache import cache
from django.test import override_settings, tag, TestCase

from src import google_apis

import asyncio
import json
import requests
from unittest import mock

google_apis_filepath = "src.google_apis"

_jwt = "jwt-highly-secure"

cache_key = "cash"


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "testing-snowflake",
        }
    }
)
@tag("fast", "logic", "unit", "purchases", "android")
@mock.patch(
    f"{google_apis_filepath}.jwt.get_jwt",
    name="get jwt",
    autospec=True,
    return_value=_jwt,
)
@mock.patch(
    f"{google_apis_filepath}.requests.post",
    name="Post",
    autospec=True,
)
class GetGoogleAccessTokenTests(TestCase):
    access_token = "secret123"
    expires_in = 1234

    def tearDown(self) -> None:
        super().tearDown()
        cache.clear()

    def _configure_post_mock(self, post_mock: mock.MagicMock) -> None:
        response = requests.Response()
        response._content = json.dumps(
            {"access_token": self.access_token, "expires_in": self.expires_in}
        ).encode()
        post_mock.return_value = response

    def test_returns_token(
        self,
        post_mock: mock.MagicMock,
        _: mock.MagicMock,
    ) -> None:
        self._configure_post_mock(post_mock)
        self.assertEqual(
            google_apis.get_access_token(
                "foo@bar.com",
                ["android publisher plz"],
                "---123encryptme---",
                cache_key,
            ),
            self.access_token,
        )

    @mock.patch(
        f"{google_apis_filepath}.cache.get",
        autospec=True,
        name="Cache get",
    )
    def test_respects_cache(
        self,
        cache_get_mock: mock.MagicMock,
        post_mock: mock.MagicMock,
        _: mock.MagicMock,
    ) -> None:
        def side_effect(passed_cache_key: str) -> None:
            self.assertEqual(passed_cache_key, cache_key)

        google_apis.get_access_token(
            "foo@bar.com",
            ["android publisher plz"],
            "---123encryptme---",
            cache_key,
        )
        post_mock.assert_not_called()

    @mock.patch(
        f"{google_apis_filepath}.cache.set",
        autospec=True,
        name="Cache set",
    )
    def test_cache_timeout(
        self,
        cache_set_mock: mock.MagicMock,
        post_mock: mock.MagicMock,
        _: mock.MagicMock,
    ) -> None:
        self._configure_post_mock(post_mock)
        google_apis.get_access_token(
            "foo@bar.com",
            ["android publisher plz"],
            "---123encryptme---",
            cache_key,
        )
        self.assertEqual(cache_set_mock.call_count, 1)
        call_args, call_kwargs = cache_set_mock.call_args_list[0]
        self.assertEqual(call_kwargs["timeout"], self.expires_in - 10)

    def test_caching(
        self,
        post_mock: mock.MagicMock,
        _: mock.MagicMock,
    ) -> None:
        self._configure_post_mock(post_mock)

        async def get_access_token() -> None:
            await asyncio.sleep(0)
            google_apis.get_access_token(
                "foo@bar.com",
                ["android publisher plz"],
                "---123encryptme---",
                cache_key,
            )
            await asyncio.sleep(0)

        async def get_access_token_many_times() -> None:
            tasks = [asyncio.create_task(get_access_token()) for x in range(100)]
            await asyncio.gather(*tasks)

        asyncio.run(get_access_token_many_times())
        post_mock.assert_called_once()
