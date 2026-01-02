from sqlmodel import SQLModel,Field,Column
import uuid
from datetime import datetime,date
import sqlalchemy.dialects.postgresql as pg


class shoe(SQLModel,table=True):
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
        created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
        updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))


        def __repr__(self):
                return f"<shoe name= {self.name}>"