from sqlalchemy import ForeignKey, create_engine,String,select
from typing import List
from sqlalchemy.orm import relationship,Mapped, mapped_column, Session
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

for i in range(10):
    p = Product(
        id = generate_uuid(),
        name="product"+str(i),
        price=i
    )
    s.add(p)
    u = User(
        id = generate_uuid(),
        name = "test"+str(i),
        email = "test@gmail.com"+str(i)
    )
    s.add(u)
s.commit()  

get_user_id = input("Enter the user_id:")
user = s.query(User).filter_by(id=get_user_id).first()
if user:
    all_products = s.query(Product).all()
    print("All Products:")
    for product in all_products:
        print ("Product ID:", product.id,"Name:", product.name,"Price:", product.price)
    get_product_id = input("Enter the product id:")
    product = s.query(Product).filter_by(id=get_product_id).first()
    if product:
        up = UserProducts(
        user_id= user.id,
        product_id=product.id)
    s.add_all([u, p, up])
    s.commit()
