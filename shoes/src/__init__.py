from fastapi import FastAPI
from src.shoes.routes import shoe_router

version='v1'

app=FastAPI(
    title="shoe_collecton",
    description="a rest api for shoe collection app",

    version= version
)

app.include_router(shoe_router,prefix=f"/api/{version}/shoes",tags=['shoes'])