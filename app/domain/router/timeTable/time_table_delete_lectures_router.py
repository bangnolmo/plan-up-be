from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.domain.oauth.google.google_service import (
    TOKEN_OK, 
    TOKEN_ERROR,
    TOKEN_EXPIRE,
    refresh_user
)
from app.utils.StatusCode import StatusCode
from app.utils.db_driver import delete_time_table_lectures_by_idx
from app.domain.exceptions.route_exceptions import TimetableNotFoundException as e_1
from app.domain.exceptions.route_exceptions import InvalidDataFormatException as e_2
from app.domain.exceptions.token_exceptoins import TokenExpiredException as e_token_expire
from app.domain.exceptions.token_exceptoins import InvaildTokenException as e_token_invalid

router = APIRouter()

@router.delete(
    "/timeTable/lectures",
    summary="시간표에 담긴 강의 정보 삭제 / Resp. 최지민",
    tags= ['timeTable']
    )
def delete_time_table_lectures(table_idx: int, class_idx: int, user : dict = Depends(refresh_user)):
    try:
        if user == TOKEN_OK: 
            if table_idx == 0 or class_idx == 0:
                raise e_2
            result = delete_time_table_lectures_by_idx(table_idx, class_idx)

            if result:
                return JSONResponse(
                    status_code=StatusCode.HTTP_OK,
                    content="TimeTable Lecture Deleted Successfully"
                    # content= result #디버그용
                )
            else:
                raise e_1
        elif user == TOKEN_EXPIRE:
            raise e_token_expire
        else:
            raise e_token_invalid    
        
    except e_1:
        raise HTTPException(StatusCode.HTTP_NOT_FOUND, detail=str(e_1))
    except e_2:
        raise HTTPException(StatusCode.HTTP_BAD_REQUEST, detail=str(e_2))
    except e_token_expire:
        raise HTTPException(StatusCode.HTTP_UNAUTHORIZED, detail=str(e_token_expire))
    except e_token_invalid:
        raise HTTPException(StatusCode.HTTP_UNAUTHORIZED, detail=str(e_token_invalid))