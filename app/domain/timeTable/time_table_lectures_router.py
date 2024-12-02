from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.utils.StatusCode import StatusCode
from app.utils.db_driver import select_class_by_time_table_idx
from app.domain.exceptions.route_exceptions import TimetableNotFoundException as e_1
from app.domain.exceptions.route_exceptions import InvalidDataFormatException as e_2

router = APIRouter()

@router.get(
    "/timeTable/lectures/{table_idx}",
    summary="시간표에 담긴 강의 정보 조회 / Resp. 최지민",
    tags= ['timeTable']
    )
def get_time_table_lectures(table_idx: int):
    try:
        if table_idx == 0:
            raise e_2
        result = select_class_by_time_table_idx(table_idx)

        if result:
            return JSONResponse(
                status_code=StatusCode.HTTP_OK,
                content=result
            )
        else:
            raise e_1
    except e_1:
        raise HTTPException(StatusCode.HTTP_NOT_FOUND, detail=str(e_1))
    except e_2:
        raise HTTPException(StatusCode.HTTP_BAD_REQUEST, detail=str(e_2))