from fastapi import APIRouter
from deta import Deta
from pydantic import BaseModel
from typing import Optional
import json

with open('settings.json') as f:
    ENV_KEYS = json.load(f)
    PROJECT_KEY = ENV_KEYS['PROJECT_KEY']
    DB_THESIS = ENV_KEYS['DB_THESIS']
    DB_AUTHORS_MASTER = ENV_KEYS['DB_AUTHORS_MASTER']
    DB_AUTHORS = ENV_KEYS['DB_AUTHORS']

DETA = Deta(PROJECT_KEY)
THESIS = DETA.Base(DB_THESIS)
AUTHORS_MASTER = DETA.Base(DB_AUTHORS_MASTER)
# {
#     'key': str,
#     'author_name': str
# }
AUTHORS = DETA.Base(DB_AUTHORS)
# {
#     'key': str
#     'thesis_id': str
#     'author_id': str
# }

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
    author_names = thesis_data.authors
    thesis_id = thesis_data.key
    author_id = ''
    authors = []
    for author_name in author_names:
        is_exist_author = len(AUTHORS_MASTER.fetch({ 'author_name': author_name })) != 0
        if is_exist_author:
            author_id = AUTHORS_MASTER.fetch({ 'author_name': author_name })[0]['key']
        else:
            author_id = AUTHORS_MASTER.put({ 'author_name': author_name })['key']

        author = AUTHORS.put({
            'thesis_id': thesis_id,
            'author_id': author_id
        })

        authors.append({
            'thesis_id': author['thesis_id'],
            'author_id': author['author_id']
        })

    thesis = THESIS.put(
        {
            'title': thesis_data.title,
            'language': thesis_data.language,
            'publish_date': thesis_data.publish_date,
            'url': thesis_data.url,
            'is_read': thesis_data.is_read,
            'page': thesis_data.page,
            'authors': authors
        },
        thesis_data.key
    )

    return thesis
