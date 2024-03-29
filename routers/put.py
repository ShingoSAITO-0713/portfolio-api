from fastapi import APIRouter
from deta import Deta
from pydantic import BaseModel
import json
from typing import Optional

with open('settings.json') as f:
    ENV_KEYS = json.load(f)
    DETA = Deta(ENV_KEYS['PROJECT_KEY'])
    THESIS = DETA.Base(ENV_KEYS['DB_THESIS'])

class ThesisData(BaseModel):
    key: str
    title: str
    language: int
    publish_date: str
    url: str
    is_read: Optional[str]
    page: Optional[str]

router = APIRouter(
    prefix='/put',
    tags=['put']
)

@router.put('/')
async def put_data(thesis_data: ThesisData):
    thesis = THESIS.put({
        'title': thesis_data.title,
        'language': thesis_data.language,
        'publish_date': thesis_data.publish_date,
        'url': thesis_data.url,
        'is_read': thesis_data.is_read,
        'page': thesis_data.page,
    }, thesis_data.key)

    return thesis