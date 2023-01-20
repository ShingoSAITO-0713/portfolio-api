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
    authors: Optional[list]
    magazine: Optional[str]
    page: Optional[str]

router = APIRouter(
    prefix='/put',
    tags=['put']
)

@router.put('/')
async def put_data(thesis_data: ThesisData):
    return thesis_data