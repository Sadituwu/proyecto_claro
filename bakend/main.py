from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import sqlite3
import joblib
import os

app = Flask(__name__)
CORS(app)

# Carga de herramientas
modelo = joblib.load('modelo_claro.pkl')
scaler = joblib.load('scaler_claro.pkl')
encoders = joblib.load('encoders_claro.pkl')
columnas_X = joblib.load('columnas_X.pkl')
estabilidad_fija = joblib.load('estabilidad_modelo.pkl')

# Validacion de datos ingresados
def validar_usuario_db(username, password):
    try:
        conn = sqlite3.connect('claro_analytics.db')
        cursor = conn.cursor()
        query = "SELECT username, rol FROM usuarios WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        usuario = cursor.fetchone()
        conn.close()
        return usuario
    except Exception as e:
        print(f"Error en DB (Validación): {e}")
        return None

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    try:
        datos = request.json
        user = datos.get('username')
        passw = datos.get('password')

        if not user or not passw:
            return jsonify({'status': 'error', 'message': 'Faltan credenciales'}), 400
        # Validamos con la base de datos
        resultado = validar_usuario_db(user, passw)

        if resultado:
            return jsonify({
                'status': 'success',
                'message': f'Bienvenido {resultado[0]}',
                'rol': resultado[1],
                'acceso': True
            })
        else:
            return jsonify({
                'status': 'error', 
                'message': 'Usuario o contraseña incorrectos',
                'acceso': False
            }), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
# Cerrar sesion
@app.route('/logout', methods=['POST'])
def logout():
    try:
        datos = request.json
        usuario = datos.get('username', 'Desconocido')
        
        return jsonify({
            'status': 'success',
            'message': f'Sesión cerrada para el usuario {usuario}',
            'acceso': False
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Prediccion modelo
@app.route('/predecir', methods=['POST'])
def predecir():
    try:
        datos = request.json 
        
        # Procesado para minusculas
        for k, v in datos.items():
            if isinstance(v, str): datos[k] = v.lower().strip()

        # id automatico para cliente
        conn = sqlite3.connect('claro_analytics.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clientes_claro")
        total_filas = cursor.fetchone()[0]
        nuevo_id_cliente = f"C{str(total_filas + 1).zfill(4)}"

        # texto a numerico
        df_nuevo = pd.DataFrame([datos])
        for col in ['Perfil_Pagador', 'Claro_Club']:
            df_nuevo[col] = encoders[col].transform(df_nuevo[col])
        
        # Columna y escalado
        X_nuevo = df_nuevo[columnas_X]
        X_scaled = scaler.transform(X_nuevo)

        # Modelo de prediccion y probabilidad
        pred_num = modelo.predict(X_scaled)
        probabilidades = modelo.predict_proba(X_scaled)
        confianza_dato = max(probabilidades[0]) * 100
        
        resultado = encoders['Razon_Abandono'].inverse_transform(pred_num)[0]

        # Guarda cliente en db
        query = """
        INSERT INTO clientes_claro (
            Cliente, Antiguedad_Mes, Plan_Precio, Perfil_Pagador, Cantidad_Lineas, 
            Claro_Club, Reclamos_Mes, Reclamos_Resueltos, DatosGB_Mes, Razon_Abandono
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        valores = (
            nuevo_id_cliente,
            datos['Antiguedad_Mes'], datos['Plan_Precio'], datos['Perfil_Pagador'],
            datos['Cantidad_Lineas'], datos['Claro_Club'], datos['Reclamos_Mes'],
            datos['Reclamos_Resueltos'], datos['DatosGB_Mes'], resultado
        )
        cursor.execute(query, valores)
        conn.commit()
        conn.close()

        # Respuesta
        return jsonify({
            'status': 'success',
            'cliente_id': nuevo_id_cliente,
            'prediccion': resultado.upper(),
            'confianza': f"{confianza_dato:.2f}%",
            'estabilidad': f"{estabilidad_fija * 100:.2f}%"
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    try:
        # =========================
        # PARAMS
        # =========================
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        search = request.args.get('search', '')
        perfil = request.args.get('perfil', '')
        sort = request.args.get('sort', 'desc')

        offset = (page - 1) * limit

        conn = sqlite3.connect('claro_analytics.db')
        conn.row_factory = sqlite3.Row

        # =========================
        # WHERE DINÁMICO
        # =========================
        where_clauses = []
        params = []

        # SEARCH
        if search:
            where_clauses.append("""
                (Cliente LIKE ? OR
                 Perfil_Pagador LIKE ? OR
                 Razon_Abandono LIKE ?)
            """)
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])

        # PERFIL
        if perfil:
            where_clauses.append("Perfil_Pagador = ?")
            params.append(perfil)

        where_sql = ""
        if where_clauses:
            where_sql = "WHERE " + " AND ".join(where_clauses)

        # =========================
        # ORDER BY
        # =========================
        order_sql = "ORDER BY Plan_Precio DESC" if sort == "desc" else "ORDER BY Plan_Precio ASC"

        # =========================
        # TOTAL (con filtros)
        # =========================
        total_query = f"""
            SELECT COUNT(*) as total
            FROM clientes_claro
            {where_sql}
        """

        total = pd.read_sql_query(total_query, conn, params=params).iloc[0, 0]

        # =========================
        # DATA PAGINADA
        # =========================
        query = f"""
            SELECT *
            FROM clientes_claro
            {where_sql}
            {order_sql}
            LIMIT ? OFFSET ?
        """

        final_params = params + [limit, offset]

        df = pd.read_sql_query(query, conn, params=final_params)
        conn.close()

        return jsonify({
            "status": "success",
            "total": int(total),
            "page": page,
            "limit": limit,
            "data": df.to_dict(orient='records')
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
# Lanzamiento
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"Servidor Claro Analytics corriendo en puerto {port}...")
    app.run(host='0.0.0.0', port=port)
