from fastapi import APIRouter,HTTPException,status,Depends
from .schemas import Shoe, shoe_update_model,shoe_create_model,ShoeDetailModel

from typing import List
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import Shoe_Service
from src.auth.dependencies import AccessTokenBearer , RoleChecker

shoe_router=APIRouter()
shoe_service=Shoe_Service()
access_token_bearer=AccessTokenBearer()
role_checker=Depends(RoleChecker(["admin","user"]))


@shoe_router.get("/",response_model=List[Shoe],dependencies=[role_checker])
async def get_all_shoes(session:AsyncSession=Depends(get_session),token_details:dict =Depends(access_token_bearer)):
    
    shoes=await shoe_service.get_all_shoes(session)
    
    return shoes

@shoe_router.get("/user/{user_uid}",response_model=List[Shoe],dependencies=[role_checker])
async def get_user_shoes(user_uid:str,session:AsyncSession=Depends(get_session),token_details:dict =Depends(access_token_bearer),):
    
    shoes=await shoe_service.get_user_shoes(user_uid,session)
    
    return shoes

@shoe_router.post("/",status_code=status.HTTP_201_CREATED,response_model=Shoe,dependencies=[role_checker])
async def create_a_shoe(shoe_data:shoe_create_model,session:AsyncSession=Depends(get_session),token_details:dict=Depends(access_token_bearer))->dict:
      user_uid=token_details.get('user')['user_uid']
     
      new_shoe=await shoe_service.create_shoe(shoe_data,user_uid,session)
      
      return new_shoe

@shoe_router.get("/{shoe_uid}",response_model=ShoeDetailModel,dependencies=[role_checker])
async def get_shoe_from_id(shoe_uid:str,session:AsyncSession=Depends(get_session),token_details:dict=Depends(access_token_bearer)) -> dict:
    Shoe=await shoe_service.get_shoe(shoe_uid,session)
    if Shoe:
        return Shoe
    
    else:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"no Shoe with id {shoe_uid}"
    )

    

@shoe_router.patch("/{shoe_uid}",response_model=Shoe,dependencies=[role_checker])
async def update_shoe(shoe_uid:str,shoe_update_data:shoe_update_model,session:AsyncSession=Depends(get_session),token_details:dict=Depends(access_token_bearer))->dict:
    updated_shoe=await shoe_service.update_shoe(shoe_uid,shoe_update_data,session)
    if updated_shoe is not None:
        return updated_shoe

    else:
        raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail=f"no Shoe found with Shoe id-{shoe_uid}"
    ) 

            
    
       
@shoe_router.delete("/{shoe_uid}",dependencies=[role_checker])
async def delete_shoe(shoe_uid:str,session:AsyncSession=Depends(get_session),token_details:dict=Depends(access_token_bearer))->dict:
    shoe_to_delete=await shoe_service.delete_shoe(shoe_uid,session)
    if shoe_to_delete is not None:
        return {}
    
    else:
        raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail=f"no Shoe found with Shoe id-{shoe_uid}"
    ) 
    
    