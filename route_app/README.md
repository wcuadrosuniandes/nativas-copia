# Gestión de trayectos

El servicio de gestión de trayectos permite crear , consultar y eliminar trayectos.

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
│   │   └── route.py # Define la entidad de usuario utilizando SQLModel, así como entidades FastAPI Request/Response relacionadas.
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
 <summary><code>POST</code> <code><b>/routes</b></code> <code>(Crear Trayecto)</code></summary>

#### Descripción

Crea un trayecto con los datos brindados

#### Cuerpo

> | Nombre               | Requerido | Tipo   | Descripción                       |
> | -------------------- | --------- | ------ | --------------------------------  |
> | flightId             | si        | string | código del vuelo                  |
> | sourceAirportCode    | si        | string | código del aeropuerto de origen   |
> | sourceCountry        | si        | string | nombre del país de origen         |
> | destinyAirportCode   | si        | string | código del aeropuerto de destino  |
> | destinyCountry       | si        | string | nombre del país de destino        |
> | bagCost              | si        |  int   | costo de envío de maleta          |
> | plannedStartDate     | si        | string | fecha hora de inicio trayecto     |
> | plannedEndDate       | si        | string | fecha hora  fin trayecto          |

#### Respuestas

> | http code | content-type       | response                                                                                                                          |
> | --------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
> | `400`     | `application/json` | Objeto con indicación de campo con error                                                                                          |
> | `412`     | `application/json` | <pre lang="json">{&#13; "detail": "Ya existe un trayecto con ese flightid"&#13;}</pre>                                            |
> | `201`     | `application/json` | <pre lang="json">{&#13; "id": "29c08ee4-2c42-4171-9149-3bfe0620be8e",&#13; "createdAt": "2024-02-04T06:25:35.781980" &#13;}</pre> |

</details>

<br/>

<details>
 <summary><code>GET</code> <code><b>/routes?flight={flightId}</b></code> <code>(Ver y filtrar trayectos)</code></summary>

#### Descripción

Retorna todos los trayectos o aquellos que corresponden a los parámetros de búsqueda. Solo un usuario autorizado puede realizar esta operación.

#### Parámetros

> | Método      |  GET                           |
> | Ruta        |  /routes?flight={flightId}     |
> | Parámetros  |  flightId: id del vuelo        |
> | Encabezados	|  Authorization: Bearer token   |
> |  Cuerpo	    |  N/A                           |

#### Respuesta

> | http code | content-type       | response                                                                    |
> | --------- | ------------------ | --------------------------------------------------------------------------- |
> | `401`     | `application/json` | El token no es válido o está vencido                                        |
> | `403`     | `application/json` | No hay token en la solicitud      |
> | `400`     | `application/json` |       |
> | `200`     | `application/json` | <pre lang="json"> [{ &#13; "id": id del trayecto, &#13; "flightId": código del vuelo, &#13; "sourceAirportCode": código del aeropuerto de origen,&#13; "sourceCountry": nombre del país de origen, &#13; "destinyAirportCode": código del aeropuerto de destino, &#13; "destinyCountry": nombre del país de destino, &#13; "bagCost": costo de envío de maleta, &#13; "plannedStartDate": fecha y hora de inicio del trayecto, &#13; "plannedEndDate": fecha y hora de finalización del trayecto, &#13; "createdAt": fecha y hora de creación del trayecto en formato ISO }] </pre>  |

</details>

<br/>

<details>
 <summary><code>GET</code> <code><b>/routes/{id}</b></code> <code>(Consultar un trayecto)</code></summary>

#### Descripción

Retorna un trayecto, solo un usuario autorizado puede realizar esta operación.

#### Parámetros

> | Método      |  GET                            |
> | Ruta        |  /routes/{id}                   |
> | Parámetros  |  id: identificador del trayecto |
> | Encabezados	|  Authorization: Bearer token    |
> |  Cuerpo	    |  N/A                            |

#### Respuesta

> | http code | content-type       | response   |
> | --------- | ------------------ | -----------|
> | `401`     | `application/json` |   El token no es válido o está vencido |
> | `403`     | `application/json` |   No hay token en la solicitud         |
> | `400`     | `application/json` |  |
> | `200`     | `application/json` | <pre lang="json"> [{ &#13; "id": id del trayecto, &#13; "flightId": código del vuelo, &#13; "sourceAirportCode": código del aeropuerto de origen,&#13; "sourceCountry": nombre del país de origen, &#13; "destinyAirportCode": código del aeropuerto de destino, &#13; "destinyCountry": nombre del país de destino, &#13; "bagCost": costo de envío de maleta, &#13; "plannedStartDate": fecha y hora de inicio del trayecto, &#13; "plannedEndDate": fecha y hora de finalización del trayecto, &#13; "createdAt": fecha y hora de creación del trayecto en formato ISO }] </pre>  |

</details>

<br/>

<details>
 <summary><code>Delete</code> <code><b>/routes/{id}</b></code> <code>(Eliminar un trayecto)</code></summary>

#### Descripción

Retorna un trayecto, solo un usuario autorizado puede realizar esta operación.

#### Parámetros

> | Método      |  GET                            |
> | Ruta        |  /routes/{id}                   |
> | Parámetros  |  id: identificador del trayecto |
> | Encabezados	|  Authorization: Bearer token    |
> |  Cuerpo	    |  N/A                            |

#### Respuesta

> | http code | content-type       | response   |
> | --------- | ------------------ | -----------|
> | `401`     | `application/json` |   El token no es válido o está vencido |
> | `403`     | `application/json` |   No hay token en la solicitud         |
> | `400`     | `application/json` |  El id no es un valor string con formato uuid |
> | `404`     | `application/json` |  El trayecto con ese id no existe |
> | `200`     | `application/json` | <pre lang="json"> { &#13; "id": "El trayecto fue eliminado"} </pre>  |

</details>

<br/>

<details>
 <summary><code>GET</code> <code><b>/routes/ping</b></code> <code>(Consultar salud del servicio)</code></summary>

#### Descripción

Usado para verificar el estado del servicio.

#### Respuesta

> | http code | content-type | response |
> | --------- | ------------ | -------- |
> | `200`     | `text/plain` | `pong`   |

## </details>

<br/>

<details>
 <summary><code>POST</code> <code><b>/routes/reset</b></code> <code>(Restablecer base de datos)</code></summary>

#### Descripción

Usado para limpiar la base de datos del servicio.

#### Respuesta

> | http code | content-type       | response                                                                       |
> | --------- | ------------------ | ------------------------------------------------------------------------------ |
> | `200`     | `application/json` | <pre lang="json">{&#13; "msg": "Todos los datos fueron eliminados"&#13;}</pre> |

## </details>

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
