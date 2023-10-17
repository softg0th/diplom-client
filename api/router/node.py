from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api.logic.db_interactions.node_db import NodeInteractions
from api.schemas import ValidNode


ni = NodeInteractions()

router = APIRouter(
    prefix="/node",
    tags=["nodes"]
)


@router.get('/node')
def get_nodes():
    return ni.getNodes()


@router.post('/node')
def register_node(node: ValidNode):
    if ni.createNode({'node': node}):
        return JSONResponse(content={"message": "Success!"}, status_code=200)
    return JSONResponse(content={"message": "Something broken!"}, status_code=500)


@router.delete('/node')
def delete_node(node_id: UUID):
    if ni.deleteNode(node_id):
        return JSONResponse(content={"message": "Success!"}, status_code=200)
    return JSONResponse(content={"message": "Something broken!"}, status_code=500)
