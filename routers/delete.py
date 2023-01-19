from fastapi import APIRouter
import asyncio
from deta import Deta

router = APIRouter(
    prefix='/delete',
    tags=['delete']
)

PROJECT_KEY = 'c00juf9n_NxF1PLjFxaBZJZTVQxonkHpn6tQ3ynvw'
DB_NAME = 'Thesis'

DETA = Deta(PROJECT_KEY)
DB = DETA.Base(DB_NAME)

@router.delete('/{id}')
async def delete_thesis(id: str):
    thesis = DB.get(id)
    DB.delete(id)

    return thesis