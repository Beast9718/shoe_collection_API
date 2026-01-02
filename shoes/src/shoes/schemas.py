from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime,date




class shoe(BaseModel):
        uid: uuid.UUID
        name: str
        company: str
        category: str
        price: float
        published_at: date
        stock: int
        created_at:datetime
        updated_at:datetime
        


class shoe_update_model(BaseModel):       
        name: Optional[str]
        company: Optional[str]
        category: Optional[str]
        price: Optional[float]
        published_at: Optional[date]
        stock: Optional[int]
        

class shoe_create_model(BaseModel): 
        
        name: str
        company: str
        category: str
        price: float
        published_at: date
        stock: int
        
            
        