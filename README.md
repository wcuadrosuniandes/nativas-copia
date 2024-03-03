# ENTREGA DESARROLLO DE APPS NATIVAS

## Tabla de contenido

- [Pre-requisitos para cada microservicio](#pre-requisitos-para-cada-microservicio)
- [Estructura de cada microservicio](#estructura-de-cada-microservicio)
  - [Carpeta src](#carpeta-src)
  - [Carpeta test](#carpeta-test)
- [Ejecutar un microservicio](#ejecutar-un-microservicio)
  - [Instalar dependencias](#instalar-dependencias)
  - [Variables de entorno](#variables-de-entorno)
  - [Ejecutar el servidor](#ejecutar-el-servidor)
  - [Ejecutar pruebas](#ejecutar-pruebas)
  - [Ejecutar desde Dockerfile](#ejecutar-desde-dockerfile)
- [Ejecutar Docker Compose](#ejecutar-docker-compose)
- [Ejecutar Colección de Postman](#ejecutar-colección-de-postman)

## Pre-requisitos para cada microservicio
- Python 3.11
- Docker
- Docker-compose
- Postman
- PostgreSQL
- SQLModel
- FastAPI


## Estructura de cada microservicio
Cada microservicio utiliza Python y FastAPI para ejecutar el servidor, y pytest para ejecutar las pruebas unitarias. En general, dentro de cada uno de ellos hay dos carpetas principales: `app` y `test`, así como algunos archivos de soporte.

### Archivos de soporte
- `.env.template`: Archivo de plantilla Env utilizado para definir variables de entorno. Consulte la sección  **Variables de entorno**.
- Dockerfile: Definición para construir la imagen Docker del microservicio. Consulta la sección **Ejecutar desde Dockerfile**.

### Carpeta app
Esta carpeta contiene el código y la lógica necesarios para declarar y ejecutar la API del microservicio, así como para la comunicación con la base de datos. Hay 2 carpetas principales:
- `/entities`: Esta carpeta contiene la capa de persistencia, donde se declaran los modelos que se van a persistir en la base de datos en forma de tablas, así como la definición de cada columna. Incluimos un archivo `nombre_microservicio.py` que contiene un modelo base llamado `SQLModel`, que realiza la configuración básica de una tabla e incluye las columnas `createdAt` y `updatedAt` por defecto para que puedas utilizarlo. 
- `/routes`: Esta carpeta contiene cada caso de uso que estamos implementando en nuestro microservicio, es decir, la lógica del negocio. En dicho archivo se manejó cada caso de uso teniendo en cuenta los criterios de aceptación dados para la entrega 1. 

En dicha carpeta tambien se encuentran dos archivos que hacen parte de la logica y persistencia:
- `/dependencies.py`: El archivo dependencies.py actúa como un ayudante al proporcionar instancias de la base de datos y sesiones, y en proyectos con dependencias de autenticación del usuario, facilita el llamado a dicho servicio. La utilización de dependencias en FastAPI simplifica la testeabilidad, ya que tanto los servicios de base de datos como la conexión al servicio de gestión de usuarios pueden ser sobrescritos con servicios simulados (mock).
-`/main.py`:El archivo main.py sirve como punto de entrada principal de la aplicación. Se encarga de inicializar las dependencias, crear la base de datos, instanciar las rutas (los endpoints de los servicios) y gestionar los errores de validación de FastAPI.

### Carpeta test
Esta carpeta contiene las pruebas para los componentes principales del microservicio que han sido declarados en la carpeta `/app`

## Ejecutar un microservicio
### Instalar dependencias

En el proceso de instalación de dependencias para nuestro proyecto, empleamos dos archivos distintos. El primero, llamado **requirements.txt** , se utiliza para especificar las dependencias necesarias para la aplicación que será desplegada en el contenedor Docker. El segundo archivo, denominado **requirements-test.txt**, está dedicado exclusivamente a las dependencias requeridas para realizar pruebas. De esta forma evitamos instalar librerías innecesarias en la imagen docker. Para instalar las dependencias se debe ejecutar:

```bash
$> pip install -r .\requirements.txt
```

### Variables de entorno

El servidor FastAPI y las pruebas unitarias utilizan variables de entorno para configurar las credenciales de la base de datos y encontrar algunas configuraciones adicionales en tiempo de ejecución. A alto nivel, esas variables son:
- DB_USER: Usuario de la base de datos Postgres
- DB_PASSWORD: Contraseña de la base de datos Postgres
- DB_HOST: Host de la base de datos Postgres
- DB_NAME: Nombre de la base de datos Postgres
- USERS_PATH: Para los microservicios que se comunican con el microservicio de Usuarios, necesitas especificar esta variable de entorno que contiene la URL utilizada para acceder a los endpoints de usuarios. (Ejemplo: http://localhost:3000, http://users-service)

Estas variables de entorno se encuentran en el archivo `.env.template` este archivo contiene una plantilla de la estructura que el archivo `.env.development` utilizado por el servidor FASTAPI requiere para funcionar.


### Ejecutar el servidor
Una vez que las variables de entorno estén configuradas correctamente, para ejecutar el servidor utiliza el siguiente comando:

```bash
$> cd <CARPETA_MICROSERVICIO> && uvicorn app.main:app --reload --port <PORT_TO_RUN_SERVER>

# Ejemplos

# Users
$> cd user_app && uvicorn app.main:app --reload --port 3000

# Posts
$> cd post_app && uvicorn app.main:app --reload --port 3001

# Routes
$> cd route_app && uvicorn app.main:app --reload --port 3002

# Offers
$> cd offer_app && uvicorn app.main:app --reload --port 3003

# Scores
$> cd score_app && uvicorn app.main:app --reload --port 3004

# Rf003
$> cd rf003_app && uvicorn app.main:app --reload --port 3005

# Rf004
$> cd rf004_app && uvicorn app.main:app --reload --port 3006

# Rf005
$> cd rf005_app && uvicorn app.main:app --reload --port 3007

```

### Ejecutar pruebas
Para ejecutar las pruebas unitarias de los microservicios y establecer el porcentaje mínimo de cobertura del conjunto de pruebas en 70%, ejecuta el siguiente comando, recuerde ubicarse en la carpeta del microservicio que desea ejecutar las pruebas:

```bash
pytest --cov-fail-under=70 --cov=src
pytest --cov-fail-under=70 --cov=src --cov-report=html
```

### Ejecutar desde Dockerfile
Para construir la imagen del Dockerfile en la carpeta, ejecuta el siguiente comando, recuerde ubicarse en la carpeta del microservicio que desea construir:

```bash
$> docker build . -t <NOMBRE_DE_LA_IMAGEN>
```
Y para ejecutar esta imagen construida, utiliza el siguiente comando:
```bash
$> docker run <NOMBRE_DE_LA_IMAGEN>
```

## Ejecutar Docker Compose
Para ejecutar todos los microservicios al mismo tiempo, utilizamos docker-compose para declarar y configurar cada Dockerfile de los microservicios. Para ejecutar docker-compose, utiliza el siguiente comando:
```bash
$> docker-compose -f "<RUTA_DEL_ARCHIVO_DOCKER_COMPOSE>" up --build

# Ejemplo
$> docker-compose -f "docker-compose.yml" up --build
```

## Ejecutar Colección de Postman
Para probar los servicios API expuestos por cada microservicio, hemos proporcionado una lista de colecciones de Postman que puedes ejecutar localmente descargando cada archivo JSON de colección e importándolo en Postman.

Lista de colecciones de Postman para cada entrega del proyecto:
- Entrega 1: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega1/entrega1.json
- Entrega 2: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega2/entrega2_verify_new_logic.json
- Entrega 3: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-monitor/main/entrega3/entrega3.json

Después de descargar la colección que deseas usar, impórtala en Postman utilizando el botón Import en la sección superior izquierda.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/836f6199-9343-447a-9bce-23d8c07d0338" alt="Screenshot" width="800">

Una vez importada la colección, actualiza las variables de colección que especifican la URL donde se está ejecutando cada microservicio.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/efafbb3d-5938-4bd8-bfc7-6becfccd2682" alt="Screenshot" width="800">

Finalmente, ejecuta la colección haciendo clic derecho en su nombre y haciendo clic en el botón "Run collection", esto ejecutará múltiples solicitudes API y también ejecutará algunos assertions que hemos preparado para asegurarnos de que el microservicio esté funcionando como se espera.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-base/assets/78829363/f5ca6f7c-e4f4-4209-a949-dcf3a6dab9e3" alt="Screenshot" width="800">
