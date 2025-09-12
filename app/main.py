from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.media_display_router import mediaDisplayRouter
from app.routes.auth_router import auth_router
from app.routes.user_router import user_router
from app.routes.review_router import review_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

app.include_router(mediaDisplayRouter)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(review_router)

@app.get("/")
async def root(q : str):
    return {"msg": "root is running"}

