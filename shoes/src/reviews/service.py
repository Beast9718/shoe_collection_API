from src.db.models import Review
from src.shoes.service import Shoe_Service
from src.auth.service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel
from fastapi.exceptions import HTTPException
from fastapi import status
import logging
from sqlmodel import desc,select

user_service=UserService()
shoe_service=Shoe_Service()


class ReviewService:
    async def add_review_to_shoe(self,user_email:str,shoe_uid:str,review_data:ReviewCreateModel,session:AsyncSession):
        try:
            shoe=await shoe_service.get_shoe(shoe_uid=shoe_uid,session=session)
            user=await user_service.get_user_by_email(email=user_email,session=session)
            review_data_dict=review_data.model_dump()
            new_review=Review(
                **review_data_dict
            )
            if not shoe:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="shoe not found")
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
            new_review.user=user
            new_review.shoe=shoe

            session.add(new_review)
            await session.commit()

            return new_review

        except  Exception as e:
            logging.exception(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="oops.. chudi lg gyi")
        
    async def get_review(self,review_uid:str,session:AsyncSession):
        statement= select(Review).where(Review.uid==review_uid)
        result=await session.exec(statement)
        return result.first()
    
    async def get_all_reviews(self,session:AsyncSession):
        statement=select(Review).order_by(desc(Review.created_at))
        result = await session.exec(statement)
        return result.all()
    
    async def delete_review_from_shoe(self,review_uid:str,user_email: str,session:AsyncSession):
        user=await user_service.get_user_by_email(user_email,session)
        review=await self.get_review(review_uid,session)
        await session.delete(review)
        await session.commit()

        




