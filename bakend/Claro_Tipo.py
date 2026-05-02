import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
import warnings
warnings.filterwarnings("ignore")

# CARGA DE DATASET 
df = pd.read_csv('Claro_Tipo.csv', sep=',') 
df.columns = df.columns.str.strip()

# EVITA CONFUSION ENTRE MAYUS Y MINUS
columnas_texto = ['Perfil_Pagador', 'Claro_Club', 'Reclamo_Frecuente', 'Razon_abandono']
for col in columnas_texto:
    df[col] = df[col].astype(str).str.lower().str.strip()

# CONVERTIR TEXTO A NUMERO
encoders = {}
for col in ['Perfil_Pagador', 'Claro_Club', 'Reclamo_Frecuente', 'Razon_abandono']:
    encoders[col] = LabelEncoder()
    df[col] = encoders[col].fit_transform(df[col].astype(str))

# DEFINIR VARIABLES
columnas_X = ['Antiguedad_Mes', 'Plan_Precio', 'Perfil_Pagador', 
              'Cantidad_Lineas', 'Claro_Club', 'Reclamos_mes', 
              'Reclamos_resueltos', 'DatosGB_Mes']

X = df[columnas_X]
y = df['Razon_abandono']

# ESCALADO
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=columnas_X)

# MODELO
modelo = LogisticRegression(max_iter=1000)
scores = cross_val_score(modelo, X_scaled, y, cv=3)
modelo.fit(X_scaled, y)

# RESULTADO DE PRECISION
print("\n" + "="*40)
print(f"PRECISION: {scores.mean() * 100:.2f}%")
print("-" * 40)

# PRUEBA CLIENTE
# [Antigüedad, Plan, Perfil Pagador, Lineas, Club, Reclamos, Resueltos, GB]
nuevo = pd.DataFrame([[12, 150, 0, 1, 1, 3, 1, 50]], columns=columnas_X)
nuevo_scaled = scaler.transform(nuevo)

pred = modelo.predict(nuevo_scaled)
razon = encoders['Razon_abandono'].inverse_transform(pred)

print(f"EL CLIENTE SE IRA POR: {razon[0].upper()}")
print("="*40 + "\n")

## GUARDA
#import joblib

#joblib.dump(modelo, 'modelo_claro.pkl')
#joblib.dump(scaler, 'scaler_claro.pkl')
#joblib.dump(encoders, 'encoders_claro.pkl')
#joblib.dump(columnas_X, 'columnas_X.pkl')

#print("¡Modelo y herramientas guardados")

#CARGA ENTRENAMIENTO
import joblib

modelo = joblib.load('modelo_claro.pkl')
scaler = joblib.load('scaler_claro.pkl')
encoders = joblib.load('encoders_claro.pkl')
columnas_X = joblib.load('columnas_X.pkl')

print("¡Modelo y herramientas cargados y listos para usar!")