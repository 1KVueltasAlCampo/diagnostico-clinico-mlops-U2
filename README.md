# Servicio de Diagnóstico Clínico

## El Problema
Se requiere un sistema capaz de realizar un triaje o diagnóstico clínico preliminar basado en tres indicadores numéricos vitales de un paciente: temperatura, frecuencia cardíaca y presión arterial, para determinar si su estado es "NO ENFERMO", "ENFERMEDAD LEVE", "ENFERMEDAD AGUDA" o "ENFERMEDAD CRÓNICA".

## El Propósito
El propósito de este repositorio es proporcionar un servicio web simulado de diagnóstico clínico con el objetivo principal de demostrar la correcta ingeniería de despliegue mediante la contenerización con Docker y la exposición de una API lista para ser consumida.

## Estructura del Repositorio
La carpeta principal del servicio contiene los siguientes archivos clave:
- **`app.py`**: Contiene la lógica del servidor web (Flask) y el algoritmo de decisión clínica para realizar las predicciones.
- **`templates/index.html`**: Interfaz gráfica web para que los usuarios interactúen con el modelo fácilmente.
- **`Dockerfile`**: Instrucciones para construir la imagen del contenedor Docker de la aplicación.
- **`requirements.txt`**: Dependencias de Python necesarias para ejecutar el servicio.

## Otros Detalles Importantes
- **Despliegue**: Todo el servicio está diseñado para ejecutarse dentro de un contenedor Docker, aislando su entorno y facilitando su portabilidad.
- **Acceso**: Una vez en ejecución, la aplicación expone sus servicios en el puerto `5000`.
- **Uso**: Se puede interactuar con el sistema mediante su interfaz web, o realizando peticiones a la API REST (GET o POST) en la ruta `/predecir`.
