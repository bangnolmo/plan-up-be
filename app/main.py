import uvicorn
from app.domain.router.department import department_router
from app.domain.router.lecture import lecture_router
from app.domain.router.login import login_user_router
from app.domain.router.timeTable import (
    time_table_delete_router,
    time_table_delete_lectures_router,
    time_table_get_lectures_router,
    time_table_router, 
    time_table_put_lectures_router
)
from starlette.middleware.cors import CORSMiddleware

# import utils.env_util as env
import app.utils.env_util as env  # init env
from app.utils.logging_config import setup_logger
from fastapi import FastAPI

from app.domain.db import db_router
from app.domain.oauth import oauth_router
# from app.test import test_router

# TODO : 배포시 docs_url 및 redoc_url 비활성화 시킬 것.
# app = FastAPI(docs_url=None, redoc_url=None)
logger = setup_logger()

app = FastAPI()

# set CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    env.FRONT_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 크롤링한 데이터를 받는 라우터 추가
app.include_router(db_router.router)

# 로그인 관련 라우터 추가
app.include_router(oauth_router.router)
app.include_router(login_user_router.router)

# 학과(교양 구분) 및 데이터 관련 라우터 추가
app.include_router(lecture_router.router)
app.include_router(department_router.router)

# 개발을 위한 테스트 라우터 추가
# app.include_router(test_router.client)

# 시간표 관련 라우터 추가
app.include_router(time_table_router.router)
app.include_router(time_table_get_lectures_router.router)
app.include_router(time_table_put_lectures_router.router)
app.include_router(time_table_delete_router.router)
app.include_router(time_table_delete_lectures_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=env.SERVER_PORT, reload=True)

#윈도우에서 실행시
#$env:PYTHONPATH = ".\"
#python .\app\main.
# 
# 또는
# 
# import sys
# import os
# #시스템 경로 추가
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))