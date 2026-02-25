from src.db.models import Review
from src.shoes.service import Shoe_Service
from src.auth.service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel
from fastapi.exceptions import HTTPException
from fastapi import status

user_service=UserService()
shoe_service=Shoe_Service()


class ReviewService:
    async def add_review_to_book(user_email:str,shoe_uid:str,review_data:ReviewCreateModel,session:AsyncSession):
        try:
            shoe=await shoe_service.get_shoe(shoe_uid=shoe_uid,session=session)
            user=await user_service.get_user_by_email(email=user_email,session=session)

        except  Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="oops.. chudi lg gyi")

