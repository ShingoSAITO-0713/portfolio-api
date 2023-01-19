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

#論文一覧の取得
@router.get('/')
async def get_all_thesis():
    theses = DB.fetch()
    return theses

#論文の詳細取得
@router.get('/{key}')
async def get_thesis_details(key: str):
    details = DB.get(key)
    return details

#既読 or 未読でフィルター
def filter_is_read(is_read: bool):
    theses = []
    if is_read: theses = DB.fetch({'is_read': 1}) #既読
    else: theses = DB.fetch({'is_read': 0}) #未読
    return theses

#言語でフィルター
def filter_language(language: str):
    theses = []
    if language == 'ja': theses = DB.fetch({'language': 0}) #日本語
    else: theses = DB.fetch({'language': 1}) #英語
    return theses

#論文一覧のフィルター
@router.get('/filter/{type}')
async def get_thesis_filtered(type: str):
    #既読 or 未読でフィルター
    if type in ['read', 'unread']:
        if type == 'read': #既読
            return filter_is_read(True)
        else: #未読
            return filter_is_read(False)
    #言語でフィルター
    elif type in ['ja', 'en']:
        return filter_language(type)

    return