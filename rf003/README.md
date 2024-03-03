# Creación de publicaciones 

Servicio para la creación de publicaciones.

## Índice

1. [Estructura](#estructura)
2. [Requisitos](#requisitos)
3. [Ejecución](#ejecución)
4. [Uso](#uso)
5. [Pruebas](#pruebas)
6. [Otras caracteristicas](#otras-características)
7. [Autor](#autor)

## Estructura

```bash
├── app # Contiene el código principal del servicio de creación de post
│   ├── entities # Almacena las entidades del servicio
│   │   ├── __init__.py
│   │   └── entities.py # Define la entidad de usuario utilizando SQLModel, así como entidades FastAPI Request/Response relacionadas.
│   ├── routers # Contiene las rutas del servicio
│   │   ├── __init__.py
│   │   └── rf003.py # Contiene los métodos expuestos por la ruta /posts
│   ├── __init__.py
│   ├── dependencies.py # Dependencias, pricipalmente instancia de base de datos
│   └── main.py # Punto de entrada de la aplicación
├── test # Código de pruebas
│   ├── __init__.py
│   └── conftest.py # Métodos de prueba de servicio de publicaciones
│   └── test_main.py # Métodos de prueba de servicio de publicaciones
├── .env.template # Plantilla de las variables de entorno utilizadas
├── .env.test # Plantilla de las variables de entorno utilizadas
├── Dockerfile # Archivo para construcción de la imagen docker
├── PipFile # Lista de dependencias necesarias para producción
├── Pipfile.lock # Lista de dependencias necesarias para pruebas
└── README.md # Documentación del servicio de creación de post
```

## Requisitos

- Python 3.11
- Docker
- Postman
- pipenv
  - Ejecute `pip install pipenv` para instalarlo

## Ejecución

Puede ejecutar por medio de docker-compose, las instrucciones las encontrará en este README.

Para ejecutar esto en su máquina y no por medio de docker, siga los siguientes pasos:

### Windows

1. Luego de clonar el repositorio cambie a este directorio

```powershell
cd .\rf004\
```

2. Copie el archivo `.env.template` a `env.development` y editelo según la distribución de microservicios puede mirar el archivo `docker-compose.yml` en la raiz del repositorio

```powershell
cp .\.env.template .env.development
```

3. Este proyecto hace uso de pipenv puede instalarlo así

```powershell
python -m pip install pipenv
```

4. Inicie un shell con el entorno virtual

```powershell
pipenv shell
```

5. Instale las dependencias

```powershell
pipenv install
```

6. Ejecute la aplicación (puede modificar el parámetro `--port` según su preferencia)

```bash
uvicorn app.main:app --reload --port 3005
```

### SO basados en Unix

1. Luego de clonar el repositorio cambie a este directorio

```bash
cd rf003
```

2. Copie el archivo `.env.template` a `env.development` y editelo según la distribución de microservicios puede mirar el archivo `docker-compose.yml` en la raiz del repositorio

```bash
cp .env.template .env.development
```

3. Este proyecto hace uso de pipenv puede instalarlo así

```bash
python -m pip install pipenv
```

4. Inicie un shell con el entorno virtual

```bash
pipenv shell
```

5. Instale las dependencias

```
pip install -r requirements.txt
```

6 Ejecute la aplicación (puede modificar el parámetro `--port` según su preferencia)

```bash
uvicorn app.main:app --reload --port 3005
```

## Uso

### El microservicio RF003

<details>
 <summary><code>POST</code> <code><b>/rf004/posts</b></code> <code>(Crear Publicación)</code></summary>

#### Descripción

Como usuario deseo crear publicaciones para que otros usuarios puedan ofertar por ellas.

#### Cuerpo

> | Nombre             | Requerido | Tipo     | Descripción                                                                            |
> | -----------------  | --------- | -------- | -------------------------------------------------------------------------------------- |
> | flightId           | si        | string   | Identificador del vuelo                                                                |
> | expireAt           | si        | string   | Fecha y hora máxima en la que se recibirán ofertas sobre la publicación en formato ISO |
> | plannedStartDate   | si        | datetime | Fecha y hora planeada de salida del origen en formato ISO                              |
> | plannedEndDate     | si        | datetime | Fecha y hora planeada de llegada en formato ISO                                        |
> | origin             | si        | Origin   | Código del aeropuerto de origen, Nombre del país de origen                             |
> | destiny            | si        | Destiny  | Código del aeropuerto de origen, Nombre del país de origen                             |
> | destiny            | si        | Destiny  | Costo de envío de maleta en dólares                                                    |

#### Respuestas

<table>
<tr>
<td> Código </td> <td> Descripción </td> <td> Cuerpo </td>
</tr>
<tr>
<td> 400 </td> <td> En el caso que alguno de los campos no esté presente en la solicitud, o no tenga el formato esperado.</td> <td> N/A </td>
</tr>
<tr>
<td> 401 </td> <td> El token no es válido o está vencido.</td> <td> N/A </td>
</tr>
<tr>
<td> 403 </td> <td> El token no está en la solicitud.</td> <td> N/A </td>
</tr>
<tr>
<td> 412 </td> <td> En el caso que la fecha de inicio y fin del trayecto no sean válidas; fechas en el pasado o no consecutivas.</td> <td> {
    "msg": "Las fechas del trayecto no son válidas"
} </td>
</tr>
<tr>
<td> 412 </td> <td> En el caso que la fecha de expiración no sea en el futuro o no sea válida.</td> <td> {
    "msg": "La fecha expiración no es válida"
} </td>
</tr>
<tr>
<td> 412 </td> <td>Si el usuario ya tiene otra publicación para el mismo trayecto.</td> <td> {
    "msg": "El usuario ya tiene una publicación para la misma fecha"
} </td>
</tr>
<tr>
</tr>
<tr>
<td> 201 </td>
<td> Si la creación de la publicación es exitosa.</td>
<td>

```json
{
    "data": {
       "id": id de la publicación,
       "userId": id del usuario que crea la publicación,
       "createdAt": fecha y hora de creación de la publicación en formato ISO,
       "expireAt": fecha y hora del último día en que se reciben ofertas sobre la publicación,
       "route": {
          "id": id del trayecto,
          "createdAt": fecha y hora de creación del trayecto en formato ISO,
       }
    },
    "msg": Resumen de la operación *.
}
```
</td>
</tr>
</table>

</details>

## Pruebas

Ya que hacemos uso de pipenv se deben instalar las dependencias de dev para los test

```
pipenv install --dev
```

Puede establecer un porcentaje mínimo de cobertura de código y ejecutar las pruebas con las siguientes instrucciones (con y sin reporte HTML):

```
pytest --cov-fail-under=70 --cov=app
pytest --cov-fail-under=70 --cov=app --cov-report=html
```

## Otras Características

Este proyecto está hecho con [FastAPI](https://fastapi.tiangolo.com/)

## Autor

Jenniffer González <j.gonzalezg2@uniandes.edu.co>