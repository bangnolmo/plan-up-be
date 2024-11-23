from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.utils.StatusCode import StatusCode
from app.utils.db_driver import login_user


router = APIRouter(
    prefix="/test",
    tags= ["test"]
)


@router.get("/update_user",
            summary="test for update user information")
def test_update_user(code: int):

    if code == 1:
        return JSONResponse(
            status_code=StatusCode.HTTP_OK,
            content= {'res': login_user("hello", 'world1', 'c++')}
        )
    else:
        return JSONResponse(
            status_code=StatusCode.HTTP_OK,
            content={'res': login_user("hello", 'world2', 'python')}
        )
