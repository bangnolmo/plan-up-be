import requests

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from app.utils.StatusCode import StatusCode
from app.utils.db_driver import login_user
from app.utils.env_util import GOOGLE_OAUTH_ID
from app.utils.env_util import GOOGLE_OAUTH_SECRET
from app.utils.env_util import GOOGLE_REDIRECT

from app.domain.oauth.google.google_service import get_google_token, get_google_token_info

router = APIRouter(
    prefix='/google',
    tags= ['oauth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/oauth/google/login")

@router.get(
    "/login",
    summary="Login with google auth / Resp. 안학룡",
)
def login_with_google(auth_code: str):
    """
    사용자가 준 구글 승인 코드를 사용 하여 로그인 수행.

    :param auth_code: 구글 승인 코드
    :return: {"access_token": value, "refresh_token": value, "user": value}
    """

    # access_token 요청
    token = get_google_token(auth_code)

    # auth code 값이 이상할 때
    if not token:
        return JSONResponse(
            status_code=StatusCode.HTTP_BAD_REQUEST,
            content={'res': 'check your auth code.'}
        )

    # 사용자 정보 조회 : 이 때 우리는 이메일 만 필요함
    # 따라서 토큰 조회를 통하여 이메일 획득하기.
    token_info = get_google_token_info(token['access_token'])

    # 발급 받은 token 값에 이상이 있을 때 또는 그 외
    if not token_info:
        return JSONResponse(
            status_code=StatusCode.HTTP_BAD_REQUEST,
            content={'res': 'Please try again in a few minutes.'}
        )

    user_email = token_info['email']

    # 학교 메일 검증
    if user_email.find('@kyonggi.ac.kr') == -1:
        return JSONResponse(
            status_code=StatusCode.HTTP_BAD_REQUEST,
            content={'res': f'{user_email} is not school mail!'}
        )

    access_token = token['access_token']
    refresh_token = token['refresh_token']

    # 사용자가 존재하는 경우 : 토큰을 갠신
    # 사용자가 존재하지 않는 경우 : 사용자및 토큰 저장.
    if not login_user(user_email, access_token, refresh_token):
        return JSONResponse(
            status_code=StatusCode.HTTP_INTERNAL_SERVER_ERROR,
            content={'res': f"Please try again in a few minutes."}
        )

    # 최종적으로 access_token 반환
    return JSONResponse(
        status_code=StatusCode.HTTP_OK,
        content={
            'res': 'ok!',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_email': user_email,
        }
    )


@router.get(
    "/auth",
    summary="사용자의 access token 인증 / Resp. 안학룡"
)
def auth_user(token: str = Depends(oauth2_scheme)):
    pass




@router.get("/callback",
            summary="auth token 받기 위한 callback / 임시 콜백")
def get_call_back(code: str):
    return code