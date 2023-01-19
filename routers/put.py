from fastapi import APIRouter
from deta import Deta
from pydantic import BaseModel
from typing import Optional

PROJECT_KEY = 'c00juf9n_NxF1PLjFxaBZJZTVQxonkHpn6tQ3ynvw'
DB_NAME = 'Thesis'

DETA = Deta(PROJECT_KEY)
DB = DETA.Base(DB_NAME)

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
