import asyncio

import httpx
import sqlalchemy

from api.logic.db_interactions.node_db import nodes_select, NodeTab, conn


async def ping_nodes():
    def updt(node_id):
        query = sqlalchemy.update(NodeTab).where(NodeTab.c.id == str(node_id)).values(
            available=False)
        return query

    def marked_nodes(nodes):
        mark = []
        for node in nodes:
            if node['available']:
                mark.append(node)
        return mark

    loop = asyncio.get_running_loop()
    all_nodes = await loop.run_in_executor(None, nodes_select)
    if len(all_nodes) == 0:
        return

    marked = await loop.run_in_executor(None, marked_nodes, all_nodes)
    if len(marked) == 0:
        return

    for node in marked:
        if node['available']:
            with httpx.Client() as client:
                ping = None
                client.get(url='https://example.com')
                try:
                    ping = client.get(url=f'http://{node["ip"]}')
                except httpx.ConnectError:
                    update = await loop.run_in_executor(None, updt, node['id'])
                    conn.execute(update)
                    conn.commit()
                if ping and ping.status_code != '200':
                    update = await loop.run_in_executor(None, updt)
                    conn.execute(update)
                    conn.commit()
    return
