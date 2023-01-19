from fastapi import APIRouter
from deta import Deta
import json

with open('settings.json') as f:
    ENV_KEYS = json.load(f)
    PROJECT_KEY = ENV_KEYS['PROJECT_KEY']
    DB_THESIS = ENV_KEYS['DB_THESIS']


router = APIRouter(
    prefix='/delete',
    tags=['delete']
)

DETA = Deta(PROJECT_KEY)
DB = DETA.Base(DB_THESIS)

@router.delete('/{id}')
async def delete_thesis(id: str):
    thesis = DB.get(id)
    DB.delete(id)

    return thesis