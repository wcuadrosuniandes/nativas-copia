# Consulta de publicaciones

Consulta de publicaciones
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
├── app # Contiene el código principal del servicio de gestión de trayectos
│   ├── entities # Almacena las entidades del servicio
│   │   ├── __init__.py
│   │   └── entities.py # Define las entidades FastAPI Request/Response relacionadas.
│   ├── routers # Contiene las rutas del servicio
│   │   ├── __init__.py
│   │   └── routers.py # Contiene los métodos expuestos por la ruta /routes
│   ├── __init__.py
│   ├── dependencies.py # Dependencias, pricipalmente instancia de base de datos
│   └── main.py # Punto de entrada de la aplicación
├── test # Código de pruebas
│   ├── __init__.py
│   └── test_main.py # Métodos de prueba de servicio de trayectos
├── .env.template # Plantilla de las variables de entorno utilizadas
├── Dockerfile # Archivo para construcción de la imagen docker
├── README.md # Documentación del servicio de gestión de trayectos
├── requirements.txt # Lista de dependencias necesarias para producción
└── requirements-test.txt # Lista de dependencias necesarias para pruebas
```

## Requisitos

- Python 3.11
- Docker
- Postman
- Motor de base de datos SQL: PostgreSQL

## Ejecución

Puede ejecutar por medio de docker-compose, las instrucciones las encontrará en este README.

Para ejecutar esto en su máquina y no por medio de docker, siga los siguientes pasos:

### Windows

1. Luego de clonar el repositorio cambie a este directorio

```powershell
cd .\route_app\
```

2. Copie el archivo `.env.template` a `env.development` y editelo según los datos de conexión de su base de datos

```powershell
cp .\.env.template .env.development
```

3. Cree el entorno virtual y activelo

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Instale las dependencias

```
pip install -r .\requirements.txt
```

5. Ejecute la aplicación (puede modificar el parámetro `--port` según su preferencia)

```bash
uvicorn app.main:app --reload --port 3000
```

### SO basados en Unix

1. Luego de clonar el repositorio cambie a este directorio

```powershell
cd route_app
```

2. Copie el archivo `.env.template` a `env.development` y editelo según los datos de conexión de su base de datos

```powershell
cp .env.template .env.development
```

3. Cree el entorno virtual y activelo

```powershell
python -m venv .venv
source .venv/bin/activate
```

4. Instale las dependencias

```
pip install -r requirements.txt
```

5. Ejecute la aplicación (puede modificar el parámetro `--port` según su preferencia)

```bash
uvicorn app.main:app --reload --port 3000
```

## Uso

### El API de gestión de trayectos expone los siguiente métodos
<details>
 <summary><code>GET</code> <code><b>/rf005/posts/{postId}</b></code> </summary>

#### Descripción

Como usuario deseo que cuando consulte una de mis publicaciones, estás contenga manera ordenada descendente por utilidad, las ofertas que han realizado otros usuarios, para no invertir tiempo innecesario eligiendo la mejor.

#### Parámetros

> | Método      |  GET                           |
> | Ruta        |  /rf005/posts/{postId}     |
> | Parámetros  |  postId: id del post        |
> | Encabezados	|  Authorization: Bearer token   |
> |  Cuerpo	    |  N/A                           |

#### Respuesta

> | http code | content-type       | response                                                                    |
> | --------- | ------------------ | --------------------------------------------------------------------------- |
> | `401`     | `application/json` | El token no es válido o está vencido                                        |
> | `403`     | `application/json` | El usuario no tiene permiso para ver el contenido de esta publicación.      |
> | `404`     | `application/json` | La publicación no existe.    |
> | `200`     | `application/json` | <pre lang="json"> [{ &#13; "id": identificador de la publicación, &#13; "expireAt": fecha y hora máxima en que se reciben ofertas en formato IDO, &#13; "route": { &#13; "id": identificador del trayecto, &#13; "fligthId": identificador del vuelo, &#13; "origin":{ &#13; "airportCode": código del aeropuerto de origen, &#13; "country": nombre del país de origen}, &#13; "destiny": { &#13; "airportCode": código del aeropuerto de destino, &#13; "country": nombre del país de destino }, &#13; "bagCost": costo de envío de maleta }, &#13; "plannedStartDate": fecha y hora en que se planea el inicio del viaje en formato ISO, &#13; "plannedEndDate": fecha y hora en que se planea la finalización del viaje en formato ISO, &#13; "createdAt": fecha y hora de creación de la publicación en formato ISO, &#13; "offers": [{ &#13; "id": identificador de la oferta, &#13; "userId": identificador del usuario que hizo la oferta, &#13; "description": descripción del paquete a llevar, &#13; "size": LARGE ó MEDIUM ó SMALL, &#13; "fragile": booleano que indica si es un paquete delicado o no, &#13; "offer": valor en dólares de la oferta para llevar el paquete, &#13; "score": utilidad que deja llevar este paquete en la maleta, &#13; "createdAt": fecha y hora de creación de la publicación en formato ISO  }]   }] </pre>  |

</details>

<br/>


## Pruebas

Para ejecutar las pruebas se deben instalar unas dependencias adicionales que se encuentran en el archivo requirements-test.txt

```
pip install -r requirements-txt.txt
```

Puede establecer un porcentaje mínimo de cobertura de código y ejecutar las pruebas con las siguientes instrucciones (con y sin reporte HTML):

```
pytest --cov-fail-under=70 --cov=app
pytest --cov-fail-under=70 --cov=app --cov-report=html
```

## Otras Características

Este proyecto está hecho con [FastAPI](https://fastapi.tiangolo.com/) y [SQLModel](https://sqlmodel.tiangolo.com/)

## Autor

Walter Giovanny Cuadros Rincón <w.cuadrosr@uniandes.edu.co>
