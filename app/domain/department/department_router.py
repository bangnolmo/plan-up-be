from fastapi import APIRouter, HTTPException, Query
from app.utils.db_driver import select_jojik_name
from app.domain.exceptions.route_exceptions import DepartmentNotFoundException as e

router = APIRouter()

@router.get("/department")
def fetch_department(id: str, year: int, hakgi: int):
    try:
        result = select_jojik_name(id, year, hakgi)

        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail=str(e))
    except e:
            raise HTTPException(status_code=404, detail=str(e))