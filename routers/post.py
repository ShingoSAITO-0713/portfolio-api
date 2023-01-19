from fastapi import APIRouter
from deta import Deta
from pydantic import BaseModel

router = APIRouter(
    prefix='/post',
    tags=['post']
)

PROJECT_KEY = 'c00juf9n_NxF1PLjFxaBZJZTVQxonkHpn6tQ3ynvw'
DB_NAME = 'Thesis'

DETA = Deta(PROJECT_KEY)
DB = DETA.Base(DB_NAME)

class ThesisData(BaseModel):
    title: str
    language: int
    publish_date: str
    url: str

@router.post('/')
async def post_Data(thesis_data: ThesisData):

    title = thesis_data.title
    language = thesis_data.language
    publish_date = thesis_data.publish_date
    url = thesis_data.url

    thesis = DB.put(
        {
            'title': title,
            'language': language,
            'publish_date': publish_date,
            'url': url
        }
    )

    return thesis
