from fastapi import APIRouter, HTTPException
from app.utils.db_driver import select_class_by_idx
from app.domain.exceptions.route_exceptions import InvalidLectureException as e

router = APIRouter()

@router.get("/lectures")
def fetch_lectures(idx: int):
    try:
        if idx:
            result = select_class_by_idx(idx)

            if result:
                return result
        else:
            raise HTTPException(status_code=404, detail=str(e))

    except e:
        raise HTTPException(status_code=404, detail=str(e))