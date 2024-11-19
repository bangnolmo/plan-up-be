from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.domain.db.db_dto import UpdateRequestDTO
from app.utils.env_util import CRAWL_AUTH
from app.utils.StatusCode import StatusCode
from app.utils.db_driver import update_jojik_and_classes, select_test

router = APIRouter(
    prefix='/db'
)

@router.put("/update")
def update_crawling_data(item:  UpdateRequestDTO):
    # auth 확인 하는 부분
    if item.auth and CRAWL_AUTH != item.auth and item.auth != 'test':
        return JSONResponse(
            status_code=StatusCode.HTTP_UNAUTHORIZED,
            content={"res": "need auth"}
        )

    # 데이터 정제

    tmp_DB = dict()

    # 조직 데이터 정제
    all_jojik, all_class = [], []
    for i, data in enumerate(item.jojik):
        if len(data) != 3:
            continue

        idx = (i + 1) * 10000000 + item.year * 1000 + item.hakgi * 10 + data[-1]
        tmp_DB[data[1]] = idx
        all_jojik.append((data[0], idx, data[1]))

    # 수업 데이터 추가 하기
    for data in item.classes:
        if len(data) != 10:
            continue

        if data[0] not in tmp_DB:
            continue
        all_class.append((*data[1:], tmp_DB[data[0]]))

    update_jojik_and_classes(all_jojik, all_class)

    return JSONResponse(
        status_code=StatusCode.HTTP_OK,
        content={"res": "OK!"}
    )

@router.get("/test")
def test():
    return JSONResponse(
        status_code=StatusCode.HTTP_OK,
        content={"res": select_test()}
    )