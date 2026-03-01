from pydantic import BaseModel,Field
import uuid 
from datetime import datetime
from src.shoes.schemas import Shoe
from typing import List
from src.reviews.schemas import ReviewModel

class UserCreateModel(BaseModel):
    first_name:str=Field(max_length=20)
    last_name:str=Field(max_length=20)
    username:str=Field(max_length=8)
    email:str=Field(max_length=30)
    password:str=Field(min_length=6)


class UserModel(BaseModel):
    uid : uuid.UUID
    username :str
    email :str
    first_name : str
    last_name : str
    is_verified : bool 
    password_hash : str 
    created_at : datetime
    updated_at : datetime

class UserShoesModel(UserModel):
    shoes:List[Shoe]
    reviews:List[ReviewModel]
    

class UserLoginModel(BaseModel):
    email:str=Field(max_length=30)
    password:str=Field(min_length=6)

class EmailModel(BaseModel):
    addresses:List[str]
    
class PasswordResetRequestModel(BaseModel):
    email:str

class PasswordResetConfirmModel(BaseModel):
    new_password:str
    confirm_new_password:str