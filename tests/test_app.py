import pytest
import sys
import os
import json

# Ensure app.py can be imported from parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, LOG_FILE

@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    # Setup: Limpiar el archivo de logs antes de cada prueba para mantener aislamiento
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        
    with app.test_client() as client:
        yield client
        
    # Teardown: Limpiar el archivo de logs después de cada prueba
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

# Casos 1, 2, y 3 implementados mediante parametrize para mayor eficiencia
@pytest.mark.parametrize("temperatura, frecuencia_cardiaca, presion_arterial, estado_esperado", [
    # 1. Enfermedad Terminal (Límite Superior)
    (42.0, 160.0, 230.0, "ENFERMEDAD TERMINAL"),
    
    # 2. No Enfermo (Límite Inferior/Saludable)
    (36.5, 70.0, 110.0, "NO ENFERMO"),
    
    # 3. Frontera Leve/Aguda
    # Valores que resultan en Leve (Temp > 37.5, pero menor a 39.0)
    (38.0, 80.0, 120.0, "ENFERMEDAD LEVE"),
    # Valores que cruzan exactamente la frontera a Aguda (Temp >= 39.0)
    (39.0, 80.0, 120.0, "ENFERMEDAD AGUDA"),
])
def test_prediccion_estados(client, temperatura, frecuencia_cardiaca, presion_arterial, estado_esperado):
    payload = {
        "temperatura": temperatura,
        "frecuencia_cardiaca": frecuencia_cardiaca,
        "presion_arterial": presion_arterial
    }
    response = client.post('/predecir', json=payload)
    
    assert response.status_code == 200
    data = response.get_json()
    assert "prediccion" in data
    assert data["prediccion"] == estado_esperado

# 4. Validación de Tipo de Dato (Error 400)
def test_prediccion_datos_invalidos(client):
    payload = {
        "temperatura": "fiebre", # Valor no numérico
        "frecuencia_cardiaca": 80,
        "presion_arterial": 120
    }
    response = client.post('/predecir', json=payload)
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "numéricos" in data["error"]

# 5. Persistencia de Estadísticas (Endpoint /estadisticas)
def test_persistencia_estadisticas(client):
    # Realizamos 1 predicción de NO ENFERMO
    client.post('/predecir', json={"temperatura": 36.5, "frecuencia_cardiaca": 70, "presion_arterial": 110})
    # Realizamos 2 predicciones de ENFERMEDAD LEVE
    client.post('/predecir', json={"temperatura": 38.0, "frecuencia_cardiaca": 80, "presion_arterial": 120})
    client.post('/predecir', json={"temperatura": 38.0, "frecuencia_cardiaca": 80, "presion_arterial": 120})

    response = client.get('/estadisticas')
    
    assert response.status_code == 200
    data = response.get_json()
    
    conteos = data["conteo_categorias"]
    assert conteos["NO ENFERMO"] == 1
    assert conteos["ENFERMEDAD LEVE"] == 2
    # El resto debería estar en 0
    assert conteos["ENFERMEDAD AGUDA"] == 0

# 6. Integridad de la Última Predicción
def test_integridad_ultima_prediccion(client):
    # Hacemos una predicción específica
    client.post('/predecir', json={"temperatura": 39.5, "frecuencia_cardiaca": 115, "presion_arterial": 135})

    response = client.get('/estadisticas')
    
    assert response.status_code == 200
    data = response.get_json()
    
    ultimas_5 = data["ultimas_5_predicciones"]
    assert len(ultimas_5) > 0
    # La última predicción debería estar en la primera posición (el endpoint debe retornar el orden invertido)
    assert ultimas_5[0]["prediccion"] == "ENFERMEDAD AGUDA"
    assert ultimas_5[0]["inputs"]["temperatura"] == 39.5
    assert ultimas_5[0]["inputs"]["frecuencia_cardiaca"] == 115.0

# 7. Estado inicial del Log
def test_estado_inicial_log(client):
    # El fixture ya se encarga de aislar la prueba asegurando que predictions_log.json no existe al inicio
    response = client.get('/estadisticas')
    
    # Debe retornar 200 a pesar de no haber log creado aún
    assert response.status_code == 200
    data = response.get_json()
    
    # Debe contener valores en cero
    assert "conteo_categorias" in data
    assert data["conteo_categorias"]["NO ENFERMO"] == 0
    assert data["conteo_categorias"]["ENFERMEDAD TERMINAL"] == 0
    assert len(data["ultimas_5_predicciones"]) == 0
    assert data["fecha_ultima_prediccion"] is None
