from datetime import datetime, timezone


def parse_unix_time(unix_time: int) -> datetime:
    """
    Returns a aware datetime representing the provided unix time with a timezone
    of UTC. The unix time should be in seconds, not milliseconds.
    """
    return datetime.fromtimestamp(unix_time, tz=timezone.utc)
