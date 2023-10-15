from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.schemas import ValidUser, UpdatedUser

from api.logic.user_db import UserInteractions

ui = UserInteractions()
router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@router.post('/reg')
def registrate_user(user: ValidUser):
    if ui.createUser({'user': user}):
        return JSONResponse(content={"message": "Success!"}, status_code=200)
    return JSONResponse(content={"message": "Something broken!"}, status_code=500)


@router.put('/updt/{user_id}')
def update_user(user_id: UUID, new_data: UpdatedUser, field: str):
    if ui.updateUser(user_id, new_data, field):
        return JSONResponse(content={"message": "Success!"}, status_code=200)
    return JSONResponse(content={"message": "Something broken!"}, status_code=500)


