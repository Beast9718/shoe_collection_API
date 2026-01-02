from fastapi import APIRouter,HTTPException,status,Depends
from src.shoes.schemas import shoe, shoe_update_model,shoe_create_model

from typing import List
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.shoes.service import Shoe_Service

shoe_router=APIRouter()
shoe_service=Shoe_Service()



@shoe_router.get("/",response_model=List[shoe])
async def get_all_shoes(session:AsyncSession=Depends(get_session)):
    shoes=await shoe_service.get_all_shoes(session)
    return shoes

@shoe_router.post("/",status_code=status.HTTP_201_CREATED,response_model=shoe)
async def create_a_shoe(shoe_data:shoe_create_model,session:AsyncSession=Depends(get_session))->dict:
      new_shoe=await shoe_service.create_shoe(shoe_data,session)
      
      return new_shoe

@shoe_router.get("/{shoe_uid}",response_model=shoe)
async def get_shoe_from_id(shoe_uid:str,session:AsyncSession=Depends(get_session)) -> dict:
    Shoe=await shoe_service.get_shoe(shoe_uid,session)
    if Shoe:
        return Shoe
    
    else:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"no shoe with id {shoe_uid}"
    )

    

@shoe_router.patch("/{shoe_uid}",response_model=shoe)
async def update_shoe(shoe_uid:str,shoe_update_data:shoe_update_model,session:AsyncSession=Depends(get_session))->dict:
    updated_shoe=await shoe_service.update_shoe(shoe_uid,shoe_update_data,session)
    if updated_shoe is not None:
        return updated_shoe

    else:
        raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail=f"no shoe found with shoe id-{shoe_uid}"
    ) 

            
    
       
@shoe_router.delete("/{shoe_uid}")
async def delete_shoe(shoe_uid:str,session:AsyncSession=Depends(get_session))->dict:
    shoe_to_delete=await shoe_service.delete_shoe(shoe_uid,session)
    if shoe_to_delete is not None:
        return {}
    
    else:
        raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail=f"no shoe found with shoe id-{shoe_uid}"
    ) 
    
    