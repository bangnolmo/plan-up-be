from fastapi.responses import JSONResponse
import requests
from fastapi import Depends, Header

from app.domain.oauth.google.google_dto import RefreshUserDTO
from app.utils.db_driver import update_user
from app.utils.StatusCode import StatusCode
from app.utils.env_util import GOOGLE_OAUTH_ID
from app.utils.env_util import GOOGLE_OAUTH_SECRET
from app.utils.env_util import GOOGLE_REDIRECT
from typing import List, Optional

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
TOKEN_OK = 'ok'

def verify_google_token(auth: Optional[str] = Header(None)):
    """
    access token 을 검증 함.

    :param auth: 사용자가 보낸 auth header
    :return: [status, token]
    """

    #for test
    if auth == "Bearer test_token":
        # print("auth test")
        return [TOKEN_OK, "Bearer test_token"]
    
    if auth is None or not auth.startswith("Bearer "):
        return [TOKEN_ERROR, None]

    access_token = auth.split()[1]
    token_info = get_google_token_info(access_token)

    if not token_info:
        return [TOKEN_EXPIRE, access_token]

    return [TOKEN_OK, access_token]


def refresh_google_token(email, refresh):
    """
    사용자의 refresh token으로 토큰을 갱신 함.

    :param email: 사용자 이메일
    :param refresh: 사용자 refresh token
    :return: new_access_token or None
    """

    # 새로운 access token 요청하기
    uri = 'https://oauth2.googleapis.com/token'
    data = {
        'client_id': GOOGLE_OAUTH_ID,
        'client_secret': GOOGLE_OAUTH_SECRET,
        'refresh_token': refresh,
        'grant_type': 'refresh_token',
    }
    res = requests.post(uri, data=data)

    if res.status_code != StatusCode.HTTP_OK:
        return None

    new_token = res.json().get('access_token', None)

    if not new_token:
        return None

    # 사용자 업데이트
    if update_user(email, new_token):
        return new_token

    return None

def refresh_user( res: List = Depends(verify_google_token)):
    """
    사용자의 토큰을 갱신함.

    :param data: 사용자의 이메일과 refresh token
    :param res: 사용자의 access token
    :return: None or new_access_token
    """

    if res[0] == "test_token":
        return TOKEN_OK

    if res[0] == TOKEN_OK:
        return TOKEN_OK
    elif res[0] == TOKEN_EXPIRE:
        return TOKEN_EXPIRE
    else:
        return TOKEN_ERROR
        

    # return refresh_google_token(data.email, data.refresh)