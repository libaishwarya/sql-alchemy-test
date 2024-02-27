from flask import Flask, request
from sqlalchemy import ForeignKey, create_engine, Column, String
from sqlalchemy.orm import sessionmaker,  relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid 

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

engine = create_engine("mysql+mysqlconnector://root:PASSWORD@localhost:3306/sqlalchemy_mysql")

Session = sessionmaker(bind=engine)
Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

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

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.json
        u_id = generate_uuid()
        name = data.get('name')
        email = data.get('email')
        address = data.get('address')

        new_user = User(id=u_id,name=name, email=email)
        user_address = Address(user_id=u_id,address=address)

        session = Session()
        session.add(new_user)
        session.add(user_address)
        session.commit()
        session.close()
    
        return 'User registered successfully', 200

if __name__ == '__main__':
    app.run(debug=True)
