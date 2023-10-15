import uvicorn
from fastapi import FastAPI
from api.router import registration


def get_app() -> FastAPI:
    app = FastAPI()
    return app


app = get_app()
app.include_router(registration.router)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
