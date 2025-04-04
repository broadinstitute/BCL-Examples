import requests


def obtain_session(target_audience: str) -> requests.Session:
    from ._google_session import google_session

    return google_session(target_audience)
