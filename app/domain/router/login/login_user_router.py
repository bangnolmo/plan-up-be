from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.utils.StatusCode import StatusCode
from app.utils.db_driver import login_user
from app.utils.db_driver import test_login_user
from app.domain.exceptions.route_exceptions import LoginException as e_1
from app.domain.exceptions.route_exceptions import InvalidDataFormatException as e_2

router = APIRouter()

class User(BaseModel):
    user_id: str
    ac_token: str
    re_token: str

@router.post(
    "/login",
    summary="로그인시 사용자 정보 삽입 및 토큰 업데이트 / Resp. 최지민",
    tags= ['login']
    )
def login(user: User):
    try:
        if user.user_id == "":
            raise e_2
        # result = login_user(user.user_id, user.ac_token, user.re_token)
        result = test_login_user(user.user_id, user.ac_token, user.re_token)

        if result:
            return JSONResponse(
                status_code=StatusCode.HTTP_OK,
                content={"message": "Login Successful"}
                # content= result #디버그용
            )
        else:
            raise e_1
        
    except e_1:
            raise HTTPException(StatusCode.HTTP_NOT_FOUND, detail=str(e_1))
    except e_2:
            raise HTTPException(StatusCode.HTTP_BAD_REQUEST, detail=str(e_2))