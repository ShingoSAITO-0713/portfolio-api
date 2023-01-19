from fastapi import APIRouter
from deta import Deta

router = APIRouter(
    prefix='/get',
    tags=['get']
)

PROJECT_KEY = 'c00juf9n_NxF1PLjFxaBZJZTVQxonkHpn6tQ3ynvw'
DB_NAME = 'Thesis'

DETA = Deta(PROJECT_KEY)
DB = DETA.Base(DB_NAME)

@router.get('/')
async def get_all_thesis():
    theses = DB.fetch()
    return theses

@router.get('/{key}')
async def get_thesis_details(key: str):
    details = DB.get(key)
    return details