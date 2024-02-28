from flask import Flask, request
from model import generate_uuid, User, Address,Session

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

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
