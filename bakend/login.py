from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Validacion de datos ingresados
def validar_usuario(username, password):
    try:
        conn = sqlite3.connect('claro_analytics.db')
        cursor = conn.cursor()
        
        # Busca al usuario y contraseña
        query = "SELECT username, rol FROM usuarios WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        usuario = cursor.fetchone()
        
        conn.close()
        return usuario # Retorna el usuario si existe, sino None
    except Exception as e:
        print(f"Error en DB: {e}")
        return None

@app.route('/login', methods=['POST'])
def login():
    try:
        datos = request.json
        user = datos.get('username')
        passw = datos.get('password')

        if not user or not passw:
            return jsonify({'status': 'error', 'message': 'Faltan credenciales'}), 400

        # Validamos con la base de datos
        resultado = validar_usuario(user, passw)

        if resultado:
            # Si los datos son correctos
            return jsonify({
                'status': 'success',
                'message': f'Bienvenido {resultado[0]}',
                'rol': resultado[1],
                'acceso': True
            })
        else:
            # Si los datos son incorrectos
            return jsonify({
                'status': 'error', 
                'message': 'Usuario o contraseña incorrectos',
                'acceso': False
            }), 401

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"Servidor de Login corriendo en el puerto {port}")
    app.run(host='0.0.0.0', port=port)