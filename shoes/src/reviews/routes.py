from fastapi import APIRouter
from .schemas import ReviewCreateModel
from src.db.models import User
from fastapi import Depends
from src.db.main import get_session
from src.auth.dependencies import get_current_user
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import ReviewService


review_router=APIRouter()
review_service=ReviewService()

@review_router.post("/shoe/{shoe_uid}")

async def add_review_to_shoe(shoe_uid:str,review_data:ReviewCreateModel,current_user:User=Depends(get_current_user),session:AsyncSession=Depends(get_session)):
    new_review=await review_service.add_review_to_shoe(shoe_uid=shoe_uid,review_data=review_data,user_email=current_user.email,session=session,)
    return new_review