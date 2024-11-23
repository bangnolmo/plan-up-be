from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.utils.StatusCode import StatusCode
from app.utils.db_driver import select_class_by_idx
from app.domain.exceptions.route_exceptions import InvalidLectureException as e

router = APIRouter()

@router.get("/lectures")
def fetch_lectures(idx: int):
    try:
        if idx:
            result = select_class_by_idx(idx)

            if result:
                return JSONResponse(
                    status_code=StatusCode.HTTP_OK,
                    content=result
                )
        else:
            raise HTTPException(status_code=404, detail=str(e))

    except e:
        raise HTTPException(status_code=404, detail=str(e))