from fastapi import APIRouter
from deta import Deta
from pydantic import BaseModel
from typing import Optional
import json

with open('settings.json') as f:
    ENV_KEYS = json.load(f)
    PROJECT_KEY = ENV_KEYS['PROJECT_KEY']
    DB_THESIS = ENV_KEYS['DB_THESIS']

DETA = Deta(PROJECT_KEY)
DB = DETA.Base(DB_THESIS)

router = APIRouter(
    prefix='/put',
    tags=['put']
)

class ThesisData(BaseModel):
    key: str
    title: str
    language: int
    publish_date: str
    url: str
    authors: Optional[list]
    is_read: Optional[int]
    magazine: Optional[str]
    page: Optional[str]

@router.put('/')
async def put_data(thesis_data: ThesisData):
    thesis = DB.put(
        {
            'title': thesis_data.title,
            'language': thesis_data.language,
            'publish_date': thesis_data.publish_date,
            'url': thesis_data.url,
            'is_read': thesis_data.is_read,
            'page': thesis_data.page
        },
        thesis_data.key
    )

    return thesis
