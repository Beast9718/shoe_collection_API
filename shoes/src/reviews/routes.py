from fastapi import APIRouter,HTTPException,status
from .schemas import ReviewCreateModel
from src.db.models import User
from fastapi import Depends
from src.db.main import get_session
from src.auth.dependencies import get_current_user,RoleChecker
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import ReviewService


review_router=APIRouter()
review_service=ReviewService()
user_role_checker=Depends(RoleChecker(["admin","user"]))
admin_role_checker=Depends(RoleChecker(["admin"]))

@review_router.post("/shoe/{shoe_uid}")
async def add_review_to_shoe(shoe_uid:str,review_data:ReviewCreateModel,current_user:User=Depends(get_current_user),session:AsyncSession=Depends(get_session)):
    new_review=await review_service.add_review_to_shoe(shoe_uid=shoe_uid,review_data=review_data,user_email=current_user.email,session=session,)
    return new_review

@review_router.get("/{review_uid}",dependencies=[user_role_checker])
async def get_review(review_uid:str,session:AsyncSession=Depends(get_session)):
    review=await review_service.get_review(review_uid,session)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="review not found"
        )
    return review

@review_router.get("/",dependencies=[user_role_checker])
async def get_review(session:AsyncSession=Depends(get_session)):
    reviews=await review_service.get_all_reviews(session)
    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="review not found"
        )
    return reviews

@review_router.delete("/{review_uid}",dependencies=[user_role_checker],status_code=status.HTTP_204_NO_CONTENT)
async def delete_review_from_shoe(review_uid:str,current_user:User=Depends(get_current_user),session:AsyncSession=Depends(get_session)):
    await review_service.delete_review_from_shoe(review_uid,current_user.email,session)
    return None
