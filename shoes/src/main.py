# from fastapi import FastAPI,status,HTTPException
# from pydantic import BaseModel
# from typing import List
# from typing import Optional
# fromshoe_data import shoes
# from src/schemas import shoe, shoe_update_model

# app=FastAPI()




# @app.get("/shoes",response_model=List[shoe])
# async def get_all_shoes():
#     return shoes

# @app.post("/shoes",status_code=status.HTTP_201_CREATED)
# async def create_a_shoe(shoe_data:shoe)->dict:
#       new_shoe=shoe_data.model_dump()
#       shoes.append(new_shoe)
#       return new_shoe

# @app.get("/shoes/{shoe_id}")
# async def get_shoe_from_id(shoe_id: int) -> dict:
#     for shoe in shoes:
#         if shoe["id"] == shoe_id:
#             return shoe

#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"no shoe with id {shoe_id}"
#     )

# @app.patch("/shoes/{shoe_id}")
# async def update_shoe(shoe_id:int,shoe_update_data:shoe_update_model)->dict:
#     for shoe in shoes:
#         if shoe['id']==shoe_id:
#             shoe['name']=shoe_update_data.name
#             shoe['company']=shoe_update_data.company
#             shoe['category']=shoe_update_data.category
#             shoe['price']=shoe_update_data.price
#             shoe['published_at']=shoe_update_data.published_at
#             shoe['stock']=shoe_update_data.stock

#             return shoe
#     raise HTTPException(
#          status_code=status.HTTP_404_NOT_FOUND,
#          detail=f"no shoe found with shoe id-{shoe_id}"
#     )
       
# @app.delete("/shoes/{shoe_id}")
# async def delete_shoe(shoe_id:int)->dict:
#     for shoe in shoes:
#         if shoe['id']==shoe_id:
#             shoes.remove(shoe)
#             return 

#     raise HTTPException(
#          status_code=status.HTTP_404_NOT_FOUND,
#          detail=f"no shoe found with shoe id-{shoe_id}"
#     ) 
    
    
      
