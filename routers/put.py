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
    prefix='/post/update',
    tags=['post']
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

#著者の登録と{id, name}の取得
def get_authors(author_names, thesis_id):
    authors = []
    for author_name in author_names:
        author_id = ''
        _author = AUTHORS_MASTER.fetch({
            'author_name': author_name
        })
        is_exit_author = _author._count != 0
        if is_exit_author:
            author_id = _author._items[0]['key']
        else:
            author_id = AUTHORS_MASTER.put({
                'author_name': author_name
            })['key']

        _thesis = AUTHORS.fetch({
            'author_id': author_id,
            'thesis_id': thesis_id
        })
        is_exist_thesis = _thesis._count != 0

        author = {}
        if is_exist_thesis:
            pass
        else:
            author = AUTHORS.put({
                'thesis_id': thesis_id,
                'author_id': author_id
            })

        authors.append({
            'author_name': author_name,
            'author_id': author_id
        })

    return authors


@router.post('/')
async def put_data(thesis_data: ThesisData):
    author_names = thesis_data.authors
    thesis_id = thesis_data.key

    authors = get_authors(author_names, thesis_id)

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
