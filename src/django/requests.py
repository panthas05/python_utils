from django.http import HttpRequest


def get_request_ip_address(request: HttpRequest) -> str:
    """
    See the arguments here:
    https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    And the more succinct discussion here:
    https://en.wikipedia.org/wiki/X-Forwarded-For

    Tl;dr: don't use for security sensitive stuff and know that this can be
    spoofed.
    """
    private_ip_prefixes = (
        "10.",
        "172.",
        "192.",
    )
    remote_address = (request.META.get("REMOTE_ADDR") or "").strip()
    if remote_address.startswith(private_ip_prefixes):
        remote_address = ""
    forwarded_for = [
        cleaned_address
        for addr in (request.META.get("HTTP_X_FORWARDED_FOR") or "").split(",")
        if (cleaned_address := addr.strip())
        and not cleaned_address.startswith(private_ip_prefixes)
    ]
    if forwarded_for:
        remote_address = forwarded_for[0]
    return remote_address
