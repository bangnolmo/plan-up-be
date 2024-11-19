from fastapi import APIRouter, HTTPException
from app.domain.services.lecture_service import get_lecture_by_id, get_all_lectures
from app.domain.entities.lecture import Lecture
from app.domain.exceptions.exceptions import InvalidLectureException

router = APIRouter()

@router.get("/lectures")
def fetch_lectures(id: str):
    try:
        if id:
            return get_lecture_by_id(id)    
        else:
            return get_all_lectures()

    except InvalidLectureException as e:
        raise HTTPException(status_code=404, detail=str(e))