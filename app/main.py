import uvicorn
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

import utils.env_util as env       # init env
from fastapi import FastAPI


# TODO : 배포시 docs_url 및 redoc_url 비활성화 시킬 것.
# app = FastAPI(docs_url=None, redoc_url=None)
app = FastAPI()

# set CORS
origins = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    env.FRONT_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/")
def main():
    return JSONResponse(
        status_code=200,
        content={ 'hello': 'world', 'wellcome': 'here!' }
    )

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=env.SERVER_PORT)