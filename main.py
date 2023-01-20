from fastapi import FastAPI
from routers import post, get, delete
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(post.router)
app.include_router(get.router)
app.include_router(delete.router)

origins = [
    'http://localhost:3000',
    'http://localhost',
    'https://portfolio2023-orcin.vercel.app',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"Hello": "World"}