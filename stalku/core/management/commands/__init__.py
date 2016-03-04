from re import findall

import requests
from django.conf import settings

session = requests.Session()
session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))


def _get_credentials():
    r = session.get(settings.PUBLIC_MENU_URL)
    token = findall(r'var token = "(\S*)";', r.text)[0]
    cookie = r.headers['Set-Cookie'].split(';')[0]
    return cookie, token


cookie, token = _get_credentials()
