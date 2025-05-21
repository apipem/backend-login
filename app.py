from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'

# Usuario de prueba
users = {
    "user1": {"password": "1234", "cedula": "123456789"}
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username in users and users[username]['password'] == password:
        token = jwt.encode({
            'user': username,
            'cedula': users[username]['cedula'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    
    return jsonify({'message': 'Credenciales incorrectas'}), 401

if __name__ == '__main__':
    app.run()
