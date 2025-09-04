from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.apis.user_review_db_api import userRouter
from app.apis.media_display_api import mediaDisplayRouter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

app.include_router(mediaDisplayRouter)
app.include_router(userRouter)


@app.get("/")
async def root(q : str):
    return {"msg": "root is running"}

