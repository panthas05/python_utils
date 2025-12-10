import re


def clean_email(email: str) -> str:
    cleaned_email = ""
    match = re.match(r"^([^+]+)(?:\+[^@]*)?(@.+)", email)
    if match:
        cleaned_email = f"{match.group(1)}{match.group(2)}"
    return cleaned_email
