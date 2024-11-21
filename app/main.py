import uvicorn
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

import app.utils.env_util as env  # init env
from fastapi import FastAPI

from app.domain.db import db_router
from app.domain.oauth import oauth_router

# TODO : 배포시 docs_url 및 redoc_url 비활성화 시킬 것.
# app = FastAPI(docs_url=None, redoc_url=None)
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


@app.get("/")
def main():
    return JSONResponse(
        status_code=200, content={"hello": "world", "wellcome": "here!"}
    )


# 크롤링한 데이터를 받는 라우터 추가
app.include_router(db_router.router)

# 로그인 관련 라우터 추가
app.include_router(oauth_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=env.SERVER_PORT)
