from fastapi import APIRouter
from deta import Deta
import json

with open('settings.json') as f:
    ENV_KEYS = json.load(f)
    PROJECT_KEY = ENV_KEYS['PROJECT_KEY']
    DB_THESIS = ENV_KEYS['DB_THESIS']


router = APIRouter(
    prefix='/get',
    tags=['get']
)

DETA = Deta(PROJECT_KEY)
DB = DETA.Base(DB_THESIS)

@router.get('/')
async def get_all_thesis():
    theses = DB.fetch()
    return theses

@router.get('/{key}')
async def get_thesis_details(key: str):
    details = DB.get(key)
    return details