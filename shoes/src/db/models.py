from sqlmodel import SQLModel,Field,Column,Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime,date
from typing import List,Optional



class User(SQLModel,table=True):
    __tablename__='user'
    uid : uuid.UUID=Field(
                sa_column=Column(
                        pg.UUID,
                        nullable=False,
                        primary_key=True,
                        default=uuid.uuid4
                )
    )
    username :str
    email :str
    first_name : str
    last_name : str
    role : str=Field(sa_column=Column(
        pg.VARCHAR,nullable=False,server_default="user"
    ))
    is_verified : bool = Field(default=False)
    password_hash : str =Field(exclude=True)
    created_at : datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    updated_at : datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    shoes:List["Shoe"]=Relationship(back_populates="user",sa_relationship_kwargs={'lazy':'selectin'})
    reviews:List["Review"]=Relationship(back_populates="user",sa_relationship_kwargs={'lazy':'selectin'})

    def __repr__(self):
        return f"<User {self.username}"
    







class Shoe(SQLModel,table=True):
        __tablename__="shoes"
        uid: uuid.UUID=Field(
                sa_column=Column(
                        pg.UUID,
                        nullable=False,
                        primary_key=True,
                        default=uuid.uuid4
                    
                )
        )
        name: str
        company: str
        category: str
        price: float
        published_at: date
        stock: int
        user_uid:Optional[uuid.UUID]=Field(default=None,foreign_key="user.uid")
        created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
        updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
        user:Optional[User]=Relationship(back_populates="shoes")
        reviews:List["Review"]=Relationship(back_populates="shoe",sa_relationship_kwargs={'lazy':'selectin'})


        def __repr__(self):
                return f"<Shoe name= {self.name}>"
        

class Review(SQLModel,table=True):
        __tablename__="reviews"
        uid: uuid.UUID=Field(
                sa_column=Column(
                        pg.UUID,
                        nullable=False,
                        primary_key=True,
                        default=uuid.uuid4
                    
                )
        )
        rating:int=Field(lt=5)
        review_text:str
        user_uid:Optional[uuid.UUID]=Field(default=None,foreign_key="user.uid")
        shoe_uid:Optional[uuid.UUID]=Field(default=None,foreign_key="shoes.uid")
        created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
        updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
        user:Optional[User]=Relationship(back_populates="reviews")
        shoe:Optional[Shoe]=Relationship(back_populates="reviews")


        def __repr__(self):
                return f"<Review for {self.shoe_uid} by {self.user_uid}>"
       