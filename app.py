from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)



app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'clave_secreta'

# Usuario de prueba
users = {
    "user1": {"password": "1234", "cedula": "123456789"}
}

@app.route('/login', methods=['POST'])
def login():
    logging.info("➡️ Inicio de la ruta /login")
    
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    logging.info(f"👤 Usuario recibido: {username}")

    if username in users and users[username]['password'] == password:
        token = jwt.encode({
            'user': username,
            'cedula': users[username]['cedula'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        # Convertir el token a str si es necesario
        token_str = token if isinstance(token, str) else token.decode('utf-8')
        
        logging.info("✅ Login exitoso")
        logging.info("⬅️ Fin de la ruta /login")
        return jsonify({'token': token_str})
    
    logging.warning("❌ Login fallido: Credenciales incorrectas")
    logging.info("⬅️ Fin de la ruta /login")
    return jsonify({'message': 'Credenciales incorrectas'}), 401
