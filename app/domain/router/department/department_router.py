from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from app.domain.oauth.google.google_service import (
    TOKEN_OK, 
    TOKEN_ERROR,
    TOKEN_EXPIRE,
    refresh_user
)
from app.utils.StatusCode import StatusCode
from app.utils.db_driver import select_jojik_name
from app.domain.exceptions.route_exceptions import DepartmentNotFoundException as e
from app.domain.exceptions.token_exceptoins import TokenExpiredException as e_token_expire
from app.domain.exceptions.token_exceptoins import InvaildTokenException as e_token_invalid

router = APIRouter()

@router.get(
    "/department",
    summary="id(gubun), year, hakgi 따른 조직 검색 / Resp. 최지민",
    tags= ['search data']
    )
def fetch_department(id: int, year: int, hakgi: int, user : dict = Depends(refresh_user)):
    try:
        if user == TOKEN_OK: 
            result = select_jojik_name(id, year, hakgi)

            if result:
                return JSONResponse(
                    status_code=StatusCode.HTTP_OK,
                    content=result
                )
            else:
                return JSONResponse(
                    status_code=StatusCode.HTTP_NOT_FOUND,
                    content={"message": "Data not found"}
                )
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