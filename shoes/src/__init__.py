from fastapi import FastAPI
from src.shoes.routes import shoe_router
from contextlib import asynccontextmanager
from src.db.main import init_db 
from src.auth.routes import auth_router
from src.reviews.routes import review_router

from .middleware import register_middleware


version='v1'
@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting....")
    await init_db()
    yield
    print(f"server stopped")
    
app=FastAPI(
    title="shoe_collecton",
    description="a rest api for Shoe collection app",
    

    version= version,
    docs_url=f"/api/{version}/docs",
    redoc_url=f"/api/{version}/redoc",
    contact={
        "email":"akhileshchy9910@gmail.com"
    }
)

register_middleware(app)

app.include_router(shoe_router,prefix=f"/api/{version}/shoes",tags=['shoes'])
app.include_router(auth_router,prefix=f"/api/{version}/auth",tags=['auth'])
app.include_router(review_router,prefix=f"/api/{version}/reviews",tags=['reviews'])