import requests
from fastapi import Header

from app.utils.StatusCode import StatusCode
from app.utils.env_util import GOOGLE_OAUTH_ID
from app.utils.env_util import GOOGLE_OAUTH_SECRET
from app.utils.env_util import GOOGLE_REDIRECT
from typing import Optional

def get_google_token(auth_code):
    """
    auth_code로 google에 access과 refresh token을 요청함.

    :param auth_code: 사용자의 auth_code
    :return: None, response {'access_token': str, 'refresh_token': str, ...}
    """
    uri = 'https://oauth2.googleapis.com/token'
    data = {
        'code': auth_code,
        'client_id': GOOGLE_OAUTH_ID,
        'client_secret': GOOGLE_OAUTH_SECRET,
        'redirect_uri': GOOGLE_REDIRECT,
        'grant_type': 'authorization_code',
    }
    res = requests.post(uri, data=data)

    if res.status_code != StatusCode.HTTP_OK:
        return None

    result = res.json()

    if 'access_token' not in result:
        return None

    if 'refresh_token' not in result:
        return None

    return result


def get_google_token_info(access_token):
    """
    access token 을 통하여 현재 token의 정보를 가져옴.

    :param access_token: access token
    :return: None or {'email': str, 'expires_in: int}
    """
    uri = 'https://oauth2.googleapis.com/tokeninfo'
    params = {
        'access_token': access_token
    }
    res = requests.get(uri, params=params)

    # 통신 확인
    if res.status_code != 200:
        return None

    result = res.json()

    if 'email' not in result:
        return None

    if 'expires_in' not in result:
        return None

    return {'email': result['email'], 'expires_in': int(result['expires_in'])}


TOKEN_ERROR = 'error'
TOKEN_EXPIRE = 'expire'

def verify_google_token(auth: Optional[str] = Header(None)):
    """
    access token 을 검증 함.

    :param auth: 사용자가 보낸 auth header
    :return: str
    """
    if auth is None or not auth.startswith("Bearer "):
        return TOKEN_ERROR

    access_token = auth.split()[1]
    token_info = get_google_token_info(access_token)

    if not token_info:
        return TOKEN_EXPIRE

    return access_token