from pydantic import BaseModel
from typing import Optional




class shoe(BaseModel):
        id: int
        name: str
        company: str
        category: str
        price: float
        published_at: str
        stock: int


class shoe_update_model(BaseModel):       
        name: Optional[str]
        company: Optional[str]
        category: Optional[str]
        price: Optional[float]
        published_at: Optional[str]
        stock: Optional[int]