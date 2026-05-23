from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predecir', methods=['GET', 'POST'])
def predecir():
    # Obtener los datos del request
    if request.method == 'POST':
        # Si es POST, intentar extraer JSON o Form data
        data = request.get_json(silent=True) or request.form
    else:
        # Si es GET, extraer los parámetros de la URL
        data = request.args
    
    try:
        # Extraer los 3 inputs clínicos numéricos requeridos
        temperatura = float(data.get('temperatura', 37.0))
        frecuencia_cardiaca = float(data.get('frecuencia_cardiaca', 80.0))
        presion_arterial = float(data.get('presion_arterial', 120.0))
    except (TypeError, ValueError):
        return jsonify({"error": "Los inputs (temperatura, frecuencia_cardiaca, presion_arterial) deben ser valores numéricos."}), 400

    # Lógica condicional basada en umbrales de gravedad clínica
    estado = "NO ENFERMO"
    
    # Condiciones para ENFERMEDAD TERMINAL (Riesgo vital inminente)
    if temperatura >= 41.0 or frecuencia_cardiaca >= 150 or presion_arterial >= 200:
        estado = "ENFERMEDAD TERMINAL"
    # Condiciones para ENFERMEDAD CRÓNICA (Extrema gravedad en cualquier indicador)
    elif temperatura >= 40.0 or frecuencia_cardiaca >= 130 or presion_arterial >= 180:
        estado = "ENFERMEDAD CRÓNICA"
    # Condiciones para ENFERMEDAD AGUDA (Gravedad moderada/alta)
    elif temperatura >= 39.0 or frecuencia_cardiaca >= 110 or presion_arterial >= 140:
        estado = "ENFERMEDAD AGUDA"
    # Condiciones para ENFERMEDAD LEVE (Ligeramente fuera de rango)
    elif temperatura > 37.5 or frecuencia_cardiaca > 90 or presion_arterial > 120:
        estado = "ENFERMEDAD LEVE"

    # Retornar la respuesta en formato JSON
    return jsonify({
        "inputs": {
            "temperatura": temperatura,
            "frecuencia_cardiaca": frecuencia_cardiaca,
            "presion_arterial": presion_arterial
        },
        "prediccion": estado
    })

if __name__ == '__main__':
    # La aplicación corre en el puerto 5000 y escucha en todas las interfaces de red (0.0.0.0)
    app.run(host='0.0.0.0', port=5000)
