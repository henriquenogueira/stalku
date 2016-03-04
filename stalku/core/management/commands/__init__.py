from re import findall
from requests import get

PUBLIC_MENU_URL = 'http://www.daconline.unicamp.br/altmatr/menupublico.do'

def _get_credentials():
    r = get(PUBLIC_MENU_URL)
    token = findall(r'var token = "(\S*)";', r.text)[0]
    cookie = r.headers['Set-Cookie'].split(';')[0]
    return cookie, token

cookie, token = _get_credentials()
