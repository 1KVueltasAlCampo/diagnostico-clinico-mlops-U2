# Servicio de Diagnóstico Clínico (Triaje MLOps)

## Contexto y Propósito (El Problema)

Este proyecto aborda el reto clínico de predecir enfermedades comunes y huérfanas basándose en síntomas, superando el problema de la escasez de datos mediante un enfoque estructurado de MLOps y simulaciones clínicas robustas. Con el fin de facilitar la adopción tecnológica en entornos médicos, este repositorio contiene el microservicio de diagnóstico empaquetado para que los médicos puedan consumirlo de manera inmediata y confiable.

Como entregable técnico de la Fase 2 del taller de MLOps, este proyecto implementa un servicio web simulado y contenerizado que proporciona predicciones de diagnóstico (clasificando en 5 estados posibles, incluyendo ENFERMEDAD TERMINAL) basadas en tres indicadores clínicos numéricos del paciente (temperatura, frecuencia cardíaca y presión arterial). El objetivo principal es demostrar la correcta implementación de la ingeniería de despliegue mediante Docker, exponiendo una API robusta, validada y lista para ser consumida.

---

## Prerrequisitos del Entorno

Para ejecutar este proyecto, es estrictamente necesario contar con un motor de contenedores funcional en tu máquina local. Las instrucciones de preparación varían según el sistema operativo:

* **Entornos Linux / macOS:** Estos sistemas interactúan de forma nativa con Docker. Se puede instalar el motor base (`Docker Engine` o `Docker CLI`) directamente desde la terminal mediante el gestor de paquetes correspondiente (ej. `apt-get` o `brew`).
* **Entornos Windows:** Dado que Docker requiere un kernel de Linux, Windows utiliza WSL 2 (Windows Subsystem for Linux) como capa de compatibilidad. Existen dos vías para configurar el entorno:
  * **Opción A - Docker Desktop (Recomendada):** Es la vía más sencilla. Al instalar la aplicación [Docker Desktop](https://www.docker.com/products/docker-desktop/), esta se encarga de configurar WSL 2 de forma automática en segundo plano. Una vez instalado, puedes ejecutar todos los comandos de este tutorial directamente desde **PowerShell** o la terminal tradicional de Windows.
  * **Opción B - Instalación manual vía WSL (CLI puro):** Si prefieres evitar la interfaz gráfica y consumir menos recursos, puedes instalar directamente `Docker Engine` dentro de tu subsistema de Linux. Esta vía requiere que configures WSL 2 por tu cuenta (ej. instando Ubuntu desde la Microsoft Store) y que ejecutes los comandos de instalación (`apt-get install docker-ce`) y de este tutorial exclusivamente desde esa terminal de Linux, no desde PowerShell.

Antes de continuar con el despliegue, verifica que el servicio de Docker esté activo ejecutando el siguiente comando en la terminal que hayas elegido utilizar:

```bash
docker --version
```

---

## Estructura del Directorio y Archivos Incluidos

Presentamos a continuación la estructura del árbol de directorios de este microservicio junto con una breve explicación del propósito de cada archivo:

```text
/servicio_diagnostico
├── Dockerfile
├── README.md
├── app.py
├── requirements.txt
└── templates/
    └── index.html
```

* `app.py`: Contiene la lógica del servidor web (orquestado vía Gunicorn y Flask) y el árbol de decisión clínica para el triaje.
* `templates/index.html`: Plantilla principal del frontend web de la aplicación.
* `requirements.txt`: Declaración de las dependencias mínimas requeridas.
* `Dockerfile`: Receta de construcción de la imagen, estructurada secuencialmente para optimizar el uso de la memoria caché de Docker.
* `README.md`: Este documento de despliegue, propósito de negocio y guía técnica de uso.

---

## Guía Técnica (Instrucciones de Despliegue y Uso)

### 1. Construir la imagen de Docker

Abre tu terminal, navega hasta el directorio raíz del proyecto (donde se ubica el archivo `Dockerfile`) y ejecuta la instrucción de construcción. El parámetro `-t` asigna la etiqueta `servicio-diagnostico` a la imagen, mientras que el punto final (`.`) le indica a Docker que el contexto de construcción es el directorio actual.

```bash
docker build -t servicio-diagnostico .
```

### 2. Ejecutar el contenedor

Con la imagen ya alojada en tu registro local, debes instanciarla creando un contenedor. Este comando mapea el puerto interno 5000 del contenedor hacia el puerto 5000 de tu máquina local, permitiendo el acceso externo.

```bash
docker run -d -p 5000:5000 --name api-diagnostico servicio-diagnostico
```

*Nota técnica: La bandera `-d` (detached) ejecuta el contenedor en segundo plano, liberando tu terminal. Puedes verificar que el contenedor está activo y saludable ejecutando `docker ps`.*

### 3. Utilizar el Sistema de Triaje

Una vez levantado el contenedor, tienes distintas formas de interactuar con el sistema:

**Opción A: Interfaz Web (Recomendada para usuarios finales)**
Abre tu navegador web y navega a [http://localhost:5000](http://localhost:5000). Verás una interfaz gráfica amigable donde podrás ingresar los signos vitales del paciente y obtener el diagnóstico clínico instantáneamente sin necesidad de usar la terminal.

**Opción B: Petición POST a la API REST (Recomendada para integración de sistemas)**
El servicio se encuentra escuchando peticiones en `http://localhost:5000/predecir`. Requiere el envío de 3 variables clínicas: `temperatura`, `frecuencia_cardiaca` y `presion_arterial`.

Ejecuta el siguiente comando `curl`. *Atención usuarios de Windows: si estás usando PowerShell, el comando `curl` es un alias de `Invoke-WebRequest` que maneja el JSON de forma distinta. Te recomendamos ejecutar esto desde una terminal WSL, Git Bash, o en su defecto, ajustar las comillas de escape en PowerShell.*

```bash
curl -X POST http://localhost:5000/predecir \
     -H "Content-Type: application/json" \
     -d '{
           "temperatura": 41.5,
           "frecuencia_cardiaca": 155,
           "presion_arterial": 205
         }'
```

**Respuesta Esperada:**

```json
{
  "inputs": {
    "frecuencia_cardiaca": 155.0,
    "presion_arterial": 205.0,
    "temperatura": 41.5
  },
  "prediccion": "ENFERMEDAD TERMINAL"
}
```

**Opción C: Petición GET**
También puedes consultar el modelo directamente a través de los parámetros en la URL:

```bash
curl "http://localhost:5000/predecir?temperatura=37.0&frecuencia_cardiaca=80&presion_arterial=110"
```

---

## Monitoreo y Solución de Problemas (Troubleshooting)

### 1. Visualización de Logs en Tiempo Real

Para diagnosticar el estado del servidor web Gunicorn/Flask o validar qué endpoints y con qué parámetros se están consumiendo, puedes inspeccionar los logs del contenedor de dos maneras:

* **Vía Consola (Terminal):**
  Ejecuta el siguiente comando para ver los logs en tiempo real (`-f` para modo "follow"):
  ```bash
  docker logs -f api-diagnostico
  ```
* **Vía Docker Desktop (Recomendado en Windows/macOS):**
  1. Abre la aplicación de **Docker Desktop**.
  2. Dirígete a la pestaña **Containers**.
  3. Haz clic sobre el contenedor `api-diagnostico`.
  4. En la pestaña **Logs**, verás la consola de salida interactiva en tiempo real. Ahí se registrarán todas las peticiones entrantes de triaje y cualquier advertencia o excepción.

### 2. Problemas Comunes y Recomendaciones

* **Error: "Port 5000 is already in use" (o el contenedor se detiene de inmediato al intentar iniciarlo):**
  * *Causa:* Otra aplicación en tu máquina local (como servicios de AirPlay en macOS, u otra instancia del taller) ya tiene ocupado el puerto 5000.
  * *Solución:* Detén el proceso que usa ese puerto o cambia el puerto de salida del contenedor al ejecutarlo (por ejemplo, mapeando el puerto `8080` de tu máquina al puerto `5000` del contenedor):
    ```bash
    docker run -d -p 8080:5000 --name api-diagnostico servicio-diagnostico
    ```
    *(Si usas esta opción, podrás acceder desde tu navegador en `http://localhost:8080`)*

* **Error: "Cannot connect to the Docker daemon..."**
  * *Causa:* El servicio o motor de Docker no se está ejecutando en tu sistema actual.
  * *Solución:* Asegúrate de tener abierta la aplicación de **Docker Desktop** y confirma que el icono en la esquina inferior izquierda esté en verde (*Engine Running*).

* **Error en la petición: "Los inputs deben ser valores numéricos"**
  * *Causa:* Estás enviando parámetros ausentes, texto en lugar de números, o el payload de tu petición `curl` se deformó (común si ejecutas comandos complejos en PowerShell nativo de Windows debido al manejo de comillas dobles).
  * *Solución:* Revisa los logs de tu contenedor para validar qué datos le están llegando a la API. Se sugiere usar herramientas como Postman, la interfaz web gráfica en el navegador, o ejecutar `curl` desde terminales como Git Bash o WSL.

---

## Limpieza del Entorno (Teardown)

Una vez finalizadas las pruebas, es una buena práctica liberar los recursos de tu máquina local. Detén el proceso de ejecución y elimina el contenedor. Posteriormente, si no planeas volver a utilizar la imagen base, bórrala para liberar espacio en el disco.

```bash
# 1. Detener el contenedor activo
docker stop api-diagnostico

# 2. Eliminar el contenedor
docker rm api-diagnostico

# 3. Eliminar la imagen construida (Opcional)
docker rmi servicio-diagnostico
```
