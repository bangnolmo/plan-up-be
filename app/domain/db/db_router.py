from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.domain.db.db_dto import UpdateRequestDTO
from app.utils.env_util import CRAWL_AUTH
from app.utils.StatusCode import StatusCode
from app.database.db_driver import update_jojik_and_classes

router = APIRouter(
    prefix='/db'
)

@router.put("/update")
def update_crawling_data(item:  UpdateRequestDTO):
    # auth 확인 하는 부분
    if CRAWL_AUTH != item.auth:
        return JSONResponse(
            status_code=StatusCode.HTTP_UNAUTHORIZED,
            content={"res": "need auth"}
        )

    # 데이터 정제
    tmp_DB = dict()

    jojiks = []
    for i, data in enumerate(item.jojik):
        if len(data) != 3:
            continue

        idx = (i + 1) * 10000000 + item.year * 1000 + item.hakgi * 10 + data[-1]


    update_jojik_and_classes(item.jojik, item.classses)

    pass