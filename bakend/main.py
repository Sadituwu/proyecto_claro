from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import sqlite3
import joblib
import os

app = Flask(__name__)
CORS(app)

# 1. CARGA DE HERRAMIENTAS .pkl
modelo = joblib.load('modelo_claro.pkl')
scaler = joblib.load('scaler_claro.pkl')
encoders = joblib.load('encoders_claro.pkl')
columnas_X = joblib.load('columnas_X.pkl')
estabilidad_fija = joblib.load('estabilidad_modelo.pkl')

@app.route('/predecir', methods=['POST'])
def predecir():
    try:
        # 2. RECIBIR DATOS .JSON
        datos = request.json 
        
        # PROCESADO PARA MINUSCULA
        for k, v in datos.items():
            if isinstance(v, str): datos[k] = v.lower().strip()

        # 3. GENERAR ID DE CLIENTE AUTOMATICO
        conn = sqlite3.connect('claro_analytics.db')
        cursor = conn.cursor()
        # Consultamos de registros
        cursor.execute("SELECT COUNT(*) FROM clientes_claro")
        total_filas = cursor.fetchone()[0]
        # Crea el ID
        nuevo_id_cliente = f"C{str(total_filas + 1).zfill(4)}"

        # 4. TRADUCCION TEXTO A NUMERICO
        df_nuevo = pd.DataFrame([datos])
        for col in ['Perfil_Pagador', 'Claro_Club']:
            df_nuevo[col] = encoders[col].transform(df_nuevo[col])
        
        # SELECCION DE COLUMNAS Y ESCALADO
        X_nuevo = df_nuevo[columnas_X]
        X_scaled = scaler.transform(X_nuevo)

        # 5. MODELO DE PREDICCION Y PROBABILIDAD
        #MODELO
        pred_num = modelo.predict(X_scaled)
        # PROBABILIDAD
        probabilidades = modelo.predict_proba(X_scaled)
        confianza_dato = max(probabilidades[0]) * 100
        
        # RESULTADO numerico a texto
        resultado = encoders['Razon_Abandono'].inverse_transform(pred_num)[0]

        # 6. GUARDAR EN .DB
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

        # 7. RESPUESTA
        return jsonify({
            'status': 'success',
            'cliente_id': nuevo_id_cliente,
            'prediccion': resultado.upper(),
            'confianza': f"{confianza_dato:.2f}%",
            'estabilidad': f"{estabilidad_fija * 100:.2f}%"
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

#DESPLIEGUE
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
