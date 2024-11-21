from fastapi import APIRouter
import requests
from starlette.responses import JSONResponse

from app.utils.StatusCode import StatusCode
from app.utils.db_driver import update_user
from app.utils.env_util import GOOGLE_OAUTH_ID
from app.utils.env_util import GOOGLE_OAUTH_SECRET
from app.utils.env_util import GOOGLE_REDIRECT

router = APIRouter(
    prefix='/google',
    tags= ['oauth']
)

@router.get(
    "",
    summary="Login with google auth / Resp. 안학룡",
)
def login_with_google(auth_code: str):
    """
    사용자가 준 구글 승인 코드를 사용 하여 로그인 수행.

    :param auth_code: 구글 승인 코드
    :return: {"access_token": value, "refresh_token": value}
    """

    # access_token 요청
    uri = 'https://oauth2.googleapis.com/token'
    data = {
        'code': auth_code,
        'client_id': GOOGLE_OAUTH_ID,
        'client_secret': GOOGLE_OAUTH_SECRET,
        'redirect_uri': GOOGLE_REDIRECT,
        'grant_type': 'authorization_code',
    }
    res = requests.post(uri, data=data)

    # 통신 확인 : 실패시 google 서버 문제 이므로, HTTP_INTERNAL_SERVER_ERROR 리턴
    if res.status_code  != StatusCode.HTTP_OK:
        return JSONResponse(
            status_code=StatusCode.HTTP_INTERNAL_SERVER_ERROR,
            content={"res": "Can't connect google server!"}
        )

    # google 서버랑 통신 성공
    token_info = res.json()

    # 사용자가 보낸 assign token 값이 이상할 때
    if 'error' in token_info:
        return JSONResponse(
            status_code=StatusCode.HTTP_BAD_REQUEST,
            content={"res": "Check your assign code."}
        )

    # 사용자 정보 조회 : 이 때 우리는 이메일 만 필요함
    # 따라서 토큰 조회를 통하여 이메일 획득하기.
    uri = 'https://oauth2.googleapis.com/tokeninfo'
    params = {
        'access_token': token_info['access_token']
    }
    res = requests.get(uri, params=params)

    # 통신 확인
    if res.status_code != StatusCode.HTTP_OK:
        return JSONResponse(
            status_code=StatusCode.HTTP_INTERNAL_SERVER_ERROR,
            content={"res": "Can't connect google server!"}
        )

    user_email = res.json()['email']

    # 학교 메일 검증
    if user_email.find('@kyonggi.ac.kr') == -1:
        return JSONResponse(
            status_code=StatusCode.HTTP_BAD_REQUEST,
            content={'res': f'{user_email} is not school mail!'}
        )

    if token_info.get('refresh_token', '') == '':
        return JSONResponse(
            status_code=StatusCode.HTTP_BAD_REQUEST,
            content={'res': 'Need refresh token'}
        )

    access_token = token_info['access_token']
    refresh_token = token_info['refresh_token']

    # 사용자가 존재하는 경우 : 토큰을 갠신
    # 사용자가 존재하지 않는 경우 : 사용자및 토큰 저장.
    if not update_user(user_email, access_token, refresh_token):
        return JSONResponse(
            status_code=StatusCode.HTTP_INTERNAL_SERVER_ERROR,
            content={'res': f"Please try again in a few minutes."}
        )

    # 최종적으로 access_token 반환
    return JSONResponse(
        status_code=StatusCode.HTTP_OK,
        content={
            'res': 'ok!',
            'access_token': token_info['access_token'],
            'refresh': token_info['refresh_token'],
        }
    )



@router.get("/callback",
            summary="auth token 받기 위한 callback / 임시 콜백")
def get_call_back(code: str):
    print(code)
    return code