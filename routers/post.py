from fastapi import APIRouter
from deta import Deta
from pydantic import BaseModel
import json
from typing import Optional
from typing import Union

with open('settings.json') as f:
    ENV_KEYS = json.load(f)
    PROJECT_KEY = ENV_KEYS['PROJECT_KEY']
    DB_THESIS = ENV_KEYS['DB_THESIS']

router = APIRouter(
    prefix='/post',
    tags=['post']
)

DETA = Deta(PROJECT_KEY)
THESIS = DETA.Base(DB_THESIS)

class ThesisData(BaseModel):
    title: str
    language: int
    publish_date: str
    url: str
    page:str
    is_read:int
    magazine: str
    authors: list

@router.post('/')
async def post_Data(thesis_data: ThesisData):
    title = thesis_data.title
    language = thesis_data.language
    publish_date = thesis_data.publish_date
    url = thesis_data.url
    page = thesis_data.page
    is_read = thesis_data.is_read
    magazine = thesis_data.magazine
    authors = thesis_data.authors

    thesis = THESIS.put(
        {
            'title': title,
            'language': language,
            'publish_date': publish_date,
            'url': url,
            'page': page,
            'is_read': is_read,
            'magazine': magazine,
            'authors': authors
        }
    )

    return thesis