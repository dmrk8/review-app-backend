from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.search_router import search_router
from app.routes.auth_router import auth_router
from app.routes.user_router import user_router
from app.routes.review_router import review_router

app = FastAPI()

origins = {
    "http://localhost:5173",
    "http://127.0.0.1:8000",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

app.include_router(search_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(review_router)

@app.get("/")
async def root(q : str):
    return {"msg": "root is running"}

