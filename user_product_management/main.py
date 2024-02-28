from psutil import users
from sqlalchemy import ForeignKey, create_engine, Column, String, Integer, select
from typing import List
from sqlalchemy.orm import sessionmaker,  relationship,Mapped, mapped_column, Session
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy.dialects import mysql

engine = create_engine("mysql+mysqlconnector://root:PASSWORD@localhost:3306/user_product")

s = Session(engine)
Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = 'user'
    id:Mapped[str] = mapped_column(String(100),primary_key=True, default=generate_uuid)
    name:Mapped[str] = mapped_column(String(100))
    email:Mapped[str] = mapped_column(String(100))
    u_product:Mapped[List["UserProducts"]]= relationship(back_populates="user")

class Product(Base):
    __tablename__ = 'product'
    id:Mapped[str] = mapped_column(String(100),primary_key=True, default=generate_uuid)
    name:Mapped[str] = mapped_column(String(100))
    price:Mapped[int] = mapped_column(String(100))
    product:Mapped[List["UserProducts"]]= relationship(back_populates="product_details")

    
class UserProducts(Base):
    __tablename__ = "user_products"
    id:Mapped[str] = mapped_column(String(100),primary_key=True, default=generate_uuid)
    user_id:Mapped[str] = mapped_column(String(100),ForeignKey("user.id"))
    product_id:Mapped[str] = mapped_column(String(100),ForeignKey("product.id"))
    user:Mapped["User"]= relationship(back_populates= "u_product")
    product_details:Mapped["Product"]= relationship(back_populates="product")

Base.metadata.create_all(engine)

u_id = generate_uuid()
p_id = generate_uuid()
u = User(
    id = u_id,
    name="test",
    email="test@gmail.com"
)
p = Product(
    id = p_id,
    name="product",
    price=2
)
up = UserProducts(
    user_id= u_id,
    product_id=p_id
)

s.add_all([u, p, up])
s.commit()
print(u)

stmt = select(User).join(UserProducts.user).join(UserProducts.product_details)
print(stmt.compile(dialect=mysql.dialect()))
data = s.scalars(stmt).all()
print(data)

for r in data:
    for product in r.u_product:
        print(r.id,r.name, r.email,product.id, product.product_id,product.product_details.name )

# Base.metadata.create_all(engine)