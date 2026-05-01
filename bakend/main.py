from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import sqlite3
import joblib

app = Flask(__name__)
CORS(app)

# 1. CARGA DE HERRAMIENTAS .pkl
modelo = joblib.load('modelo_claro.pkl')
scaler = joblib.load('scaler_claro.pkl')
encoders = joblib.load('encoders_claro.pkl')
columnas_X = joblib.load('columnas_X.pkl')

@app.route('/predecir', methods=['POST'])
def predecir():
    try:
        # 2. RECIBIR DATOS .JSON
        datos = request.json 
        
        # PROCESADO PARA MINUSCULA
        for k, v in datos.items():
            if isinstance(v, str): datos[k] = v.lower().strip()

        #TEXTO A NUMERICO
        df_nuevo = pd.DataFrame([datos])
        for col in ['Perfil_Pagador', 'Claro_Club']:
            df_nuevo[col] = encoders[col].transform(df_nuevo[col])
        
        #ESCALA EL PESO
        X_nuevo = df_nuevo[columnas_X]
        X_scaled = scaler.transform(X_nuevo)

        # 4. MODELO DE PREDICCIÓN
        pred_num = modelo.predict(X_scaled)
        resultado = encoders['Razon_abandono'].inverse_transform(pred_num)[0]

        # 5. GUARDAR EN .DB
        conn = sqlite3.connect('claro_analytics.db')
        cursor = conn.cursor()
        query = """
        INSERT INTO clientes_claro (
            Antiguedad_Mes, Plan_Precio, Perfil_Pagador, Cantidad_Lineas, 
            Claro_Club, Reclamos_mes, Reclamos_resueltos, DatosGB_Mes, Razon_abandono
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        valores = (
            datos['Antiguedad_Mes'], datos['Plan_Precio'], datos['Perfil_Pagador'],
            datos['Cantidad_Lineas'], datos['Claro_Club'], datos['Reclamos_mes'],
            datos['Reclamos_resueltos'], datos['DatosGB_Mes'], resultado
        )
        cursor.execute(query, valores)
        conn.commit()
        conn.close()

        # 6. RESPUESTA
        return jsonify({
            'status': 'success',
            'prediccion': resultado.upper()
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == "__main__":
    # host='0.0.0.0' visible
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)