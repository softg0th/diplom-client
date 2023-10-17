import asyncio

import httpx
import sqlalchemy
from apscheduler.schedulers.background import BackgroundScheduler

from api.logic.db_interactions.node_db import nodes_select, NodeTab, conn

scheduler = BackgroundScheduler()


async def ping_nodes():
    loop = asyncio.get_running_loop()
    available_nodes = await loop.run_in_executor(None, nodes_select)

    if len(available_nodes) == 0:
        return -1

    for node in available_nodes:
        if node['available']:
            with httpx.Client() as client:
                ping = client.get(url=f'http://{node.ip}')
                if ping.status_code != '200':
                    update = sqlalchemy.update(NodeTab).where(NodeTab.c.id == str(node.id)).values(
                        awailable=False)
                    conn.execute(update)
                    conn.commit()
