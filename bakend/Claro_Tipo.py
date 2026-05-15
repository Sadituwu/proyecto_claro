import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import warnings
warnings.filterwarnings("ignore")

# 1. CARGA DE DATASET
df = pd.read_csv('Claro_Tipo.csv', sep=',') 
df.columns = df.columns.str.strip()

# 2. LIMPIEZA Y NORMALIZACIÓN
columnas_texto = ['Perfil_Pagador', 'Claro_Club', 'Reclamo_Frecuente', 'Razon_Abandono']
for col in columnas_texto:
    df[col] = df[col].astype(str).str.lower().str.strip()

# 3. CONVERTIR TEXTO A NÚMERO
encoders = {}
for col in columnas_texto:
    encoders[col] = LabelEncoder()
    df[col] = encoders[col].fit_transform(df[col])

# 4. DEFINIR VARIABLES (X e y)
columnas_X = ['Antiguedad_Mes', 'Plan_Precio', 'Perfil_Pagador', 
              'Cantidad_Lineas', 'Claro_Club', 'Reclamos_Mes', 
              'Reclamos_Resueltos', 'DatosGB_Mes']

X = df[columnas_X]
y = df['Razon_Abandono']

# 5. ESCALADO
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 6. MODELO Y ESTABILIDAD (Validación Cruzada)
modelo = LogisticRegression(max_iter=1000, C=0.5)
scores = cross_val_score(modelo, X_scaled, y, cv=5)
modelo.fit(X_scaled, y)

# Fix compatibilidad sklearn 1.7.x en servidor
if hasattr(modelo, 'multi_class'):
    delattr(modelo, 'multi_class')

# Calculamos la estabilidad media
estabilidad_media = scores.mean()

print("\n" + "="*40)
print(f"PRECISION MEDIA: {estabilidad_media * 100:.2f}%")
print(f"DESVIACION (Varianza): {scores.std() * 100:.2f}%")
print("-" * 40)

# 7. PRUEBA DE CLIENTE
input_cliente = {
    'Antiguedad_Mes': 12,
    'Plan_Precio': 150,
    'Perfil_Pagador': 'critico',
    'Cantidad_Lineas': 1,
    'Claro_Club': 'no',
    'Reclamos_Mes': 3,
    'Reclamos_Resueltos': 1,
    'DatosGB_Mes': 50
}

prueba = pd.DataFrame([input_cliente])
prueba['Perfil_Pagador'] = encoders['Perfil_Pagador'].transform([prueba['Perfil_Pagador'][0]])
prueba['Claro_Club'] = encoders['Claro_Club'].transform([prueba['Claro_Club'][0]])

# Escalado y Predicción
prueba_scaled = scaler.transform(prueba[columnas_X])
pred = modelo.predict(prueba_scaled)
razon = encoders['Razon_Abandono'].inverse_transform(pred)

print(f"PRUEBA: EL CLIENTE SE IRÍA POR: {razon[0].upper()}")
print("="*40 + "\n")

# 8. GUARDADO DE PKL
joblib.dump(modelo, 'modelo_claro.pkl')
joblib.dump(scaler, 'scaler_claro.pkl')
joblib.dump(encoders, 'encoders_claro.pkl')
joblib.dump(columnas_X, 'columnas_X.pkl')
joblib.dump(estabilidad_media, 'estabilidad_modelo.pkl')

print("¡Todos los archivos .pkl han sido actualizados!")