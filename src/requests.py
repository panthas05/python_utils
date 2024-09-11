import requests


def informative_raise_for_status(response: requests.Response) -> None:
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        e.add_note(response.content.decode())
        raise e
