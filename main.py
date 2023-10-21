import asyncio

import uvicorn
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from api.router import registration
from api.router import node
from tasks.availability import ping_nodes


def get_app() -> FastAPI:
    app = FastAPI()
    return app


app = get_app()
app.include_router(registration.router)
app.include_router(node.router)


async def ping_task() -> None:
    await ping_nodes()


@app.on_event('startup')
async def run_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(ping_task, 'interval', seconds=300, max_instances=1)
    scheduler.start()


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)

