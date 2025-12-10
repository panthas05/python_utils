from unittest import TestCase

from src import parsers

from datetime import datetime, timezone


class ParseUnixTimeTests(TestCase):
    unix_time_start = datetime(1970, 1, 1, tzinfo=timezone.utc)

    def test_parses_start(self) -> None:
        parsed_unix_time_start = parsers.parse_unix_time(0)
        self.assertEqual(self.unix_time_start, parsed_unix_time_start)

    def test_parses_generic(self) -> None:
        # 2023-09-28 00:00:00 UTC
        parsed_time = parsers.parse_unix_time(1695859200)
        expected_time = datetime(2023, 9, 28, tzinfo=timezone.utc)
        self.assertEqual(parsed_time, expected_time)
