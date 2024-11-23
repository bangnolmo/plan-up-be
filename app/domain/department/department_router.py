from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.domain.exceptions.route_exceptions import DepartmentNotFoundException as e
from app.utils.StatusCode import StatusCode
from app.utils.db_driver import select_jojik_name

router = APIRouter()

@router.get("/department")
def fetch_department(id: str, year: int, hakgi: int):
    try:
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
    except e:
            raise HTTPException(status_code=404, detail=str(e))