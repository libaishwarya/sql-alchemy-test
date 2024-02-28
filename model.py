from sqlalchemy import ForeignKey, create_engine, Column, String
from sqlalchemy.orm import sessionmaker,  relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid 

engine = create_engine("mysql+mysqlconnector://root:PASSWORD@localhost:3306/sqlalchemy_mysql")

Session = sessionmaker(bind=engine)

def generate_uuid():
    return str(uuid.uuid4())
Base = declarative_base()

class User(Base):
    __tablename__ = 'userTable'
    id = Column(String(225), primary_key=True, default=generate_uuid)
    name = Column(String(50))
    email = Column(String(120))  # Changed to String(120)
    addresses = relationship("Address",back_populates = "users")

class Address(Base):
    __tablename__ = 'userAddress'
    id = Column(String(225), primary_key=True, default=generate_uuid)
    user_id = Column(String(120), ForeignKey("userTable.id"))
    address = Column(String(225))
    users = relationship("User",back_populates="addresses")

Base.metadata.create_all(engine)