import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse

from api.logic.db_interactions.file_db import FileInteractions
from api.logic.cloud.upload_file_to_server import executor

router = APIRouter(
    prefix="/files",
    tags=["files"]
)

fi = FileInteractions()


@router.get('/get/')
def get(user_id):
    data = fi.get_all_files(user_id)
    return data


@router.post('/upload/')
def upload(user_id, file: UploadFile = File()):
    output = executor(user_id, file)
    if output:
        filename = Path(file.filename)
        data = fi.create_file(user_id, uuid.uuid4(), filename)
        return data
    raise HTTPException(status_code=500, detail='Nodes broken!')


@router.delete('/delete/')
def delete(user_id, file_id):
    data = fi.delete_file(user_id, file_id)
    return data


@router.put('/update/')
def update(user_id, file_id, verbose_name):
    data = fi.update_file(user_id, file_id, verbose_name)
    return data


@router.get('/load/')
def load(user_id, file_id, file_name):
    data = fi.load_file(user_id, file_id, file_name)
    return FileResponse(data)
