# Utilizamos una imagen base oficial de Python ligera
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero el archivo de requerimientos para aprovechar la caché de capas de Docker
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código fuente (app.py y plantillas)
COPY app.py .
COPY templates/ templates/

# Exponemos el puerto 5000 donde corre Flask
EXPOSE 5000

# Usar Gunicorn en lugar del servidor de desarrollo de Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
