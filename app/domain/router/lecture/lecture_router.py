from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from app.domain.oauth.google.google_service import (
    TOKEN_OK, 
    TOKEN_ERROR,
    TOKEN_EXPIRE,
    refresh_user
)
from app.utils.StatusCode import StatusCode
from app.utils.db_driver import select_class_by_idx
from app.domain.exceptions.route_exceptions import InvalidLectureException as e
from app.domain.exceptions.token_exceptoins import TokenExpiredException as e_token_expire
from app.domain.exceptions.token_exceptoins import InvaildTokenException as e_token_invalid

router = APIRouter()

@router.get(
    "/lectures",
    summary="조직에 따른 개강한 수업 조회 / Resp. 최지민",
    tags= ['search data']
    )
def fetch_lectures(idx: int, user : dict = Depends(refresh_user)):
    try:
        if user == TOKEN_OK: 
            if idx:
                result = select_class_by_idx(idx)

                if result:
                    return JSONResponse(
                        status_code=StatusCode.HTTP_OK,
                        content=result
                    )
            else:
                raise e
        elif user == TOKEN_EXPIRE:
            raise e_token_expire
        else:
            raise e_token_invalid    

    except e:
        raise HTTPException(status_code=404, detail=str(e))
    except e_token_expire:
        raise HTTPException(StatusCode.HTTP_UNAUTHORIZED, detail=str(e_token_expire))
    except e_token_invalid:
        raise HTTPException(StatusCode.HTTP_UNAUTHORIZED, detail=str(e_token_invalid))