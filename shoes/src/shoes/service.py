from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import shoe_create_model,shoe_update_model
from sqlmodel import select,desc
from src.db.models import Shoe
from datetime import datetime


class Shoe_Service:
    async def get_all_shoes(self,session:AsyncSession):
        statement=select(Shoe).order_by(desc(Shoe.created_at))
        result=await session.exec(statement)
        return result.all()
    
    async def get_user_shoes(self,user_uid:str,session:AsyncSession):
        statement=select(Shoe).where(Shoe.user_uid==user_uid).order_by(desc(Shoe.created_at))
        result=await session.exec(statement)
        return result.all()
    
    async def get_shoe(self,shoe_uid:str,session:AsyncSession):
        statement=select(Shoe).where(Shoe.uid == shoe_uid)
        result=await session.exec(statement)
        shoe= result.first()
        return shoe if shoe is not None else None
    
    async def create_shoe(self,shoe_data:shoe_create_model,user_uid:str,session:AsyncSession):
        shoe_data_dictionarie=shoe_data.model_dump()
        new_shoe=Shoe(
            **shoe_data_dictionarie
        )
        new_shoe.user_uid=user_uid
        
        # new_shoe.published_at=datetime.strptime(shoe_data_dictionarie['published_at'],"%Y-%m-%d")
        session.add(new_shoe)
        await session.commit()
        
        return new_shoe
    async def update_shoe(self,shoe_uid:str,update_data:shoe_update_model,session:AsyncSession):
        shoe_to_update=await self.get_shoe(shoe_uid,session)
        
        if shoe_to_update is not None:
           shoe_update_dictionarie=update_data.model_dump()
           for k,v in shoe_update_dictionarie.items():
               setattr(shoe_to_update,k,v)
           await session.commit()
           return shoe_to_update
        else:
            return None

    async def delete_shoe(self,shoe_uid:str,session:AsyncSession):
        shoe_to_delete=await self.get_shoe(shoe_uid,session)
        if shoe_to_delete is not None:
            await session.delete(shoe_to_delete)
            await session.commit()
            return {}
        else:
            return None