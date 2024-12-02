from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.utils.StatusCode import StatusCode
from app.utils.db_driver import create_time_table, select_time_table
from app.domain.exceptions.route_exceptions import TimetableCreationException as e_1
from app.domain.exceptions.route_exceptions import TimetableNotFoundException as e_2
from app.domain.exceptions.route_exceptions import InvalidDataFormatException as e_3

router = APIRouter()

class timeTable(BaseModel):
    name : str
    year : int
    semester : int
    owner : str

@router.post(
    "/timeTable",
    summary="시간표 생성 / Resp. 최지민",
    tags= ['timeTable']
    )
def post_timeTable(timeTable: timeTable):
    try:
        if timeTable.name == "" or timeTable.year == 0 or timeTable.semester == 0 or timeTable.owner == "":
            raise e_3
        
        result = create_time_table(timeTable.name, timeTable.year, timeTable.semester, timeTable.owner)

        if result:
            return JSONResponse(
                status_code=StatusCode.HTTP_OK,
                # content={"message": "TimeTable Created"}
                content= result #디버그용
            )
        else:
            raise e_1
    except e_1:
        raise HTTPException(StatusCode.HTTP_NOT_FOUND, detail=str(e_1))
    except e_3:
        raise HTTPException(StatusCode.HTTP_BAD_REQUEST, detail=str(e_3))
    
@router.get(
    "/timeTable",
    summary="사용자의 시간표 조회 / Resp. 최지민",
    tags= ['timeTable']
    )
def get_timeTable(email: str):
    try:
        if email == "":
            raise e_3

        result = select_time_table(email)

        if result:
            return JSONResponse(
                status_code=StatusCode.HTTP_OK,
                content=result
            )
        else:
            raise e_2
        
    except e_2:
        raise HTTPException(StatusCode.HTTP_NOT_FOUND, detail=str(e_1))
    except e_3:
        raise HTTPException(StatusCode.HTTP_BAD_REQUEST, detail=str(e_2))