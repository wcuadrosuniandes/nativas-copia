# Gestión de scores

El servicio de gestión de scores permite crear , consultar por id o todos los puntajes.

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
├── app # Contiene el código principal del servicio de gestión de puntajes
│   ├── entities # Almacena las entidades del servicio
│   │   ├── __init__.py
│   │   └── score.py # Define la entidad de usuario utilizando SQLModel, así como entidades FastAPI Request/Response relacionadas.
│   ├── routers # Contiene las rutas del servicio
│   │   ├── __init__.py
│   │   └── scores.py # Contiene los métodos expuestos con la ruta /scores
│   ├── __init__.py
│   ├── dependencies.py # Dependencias, pricipalmente instancia de base de datos
│   └── main.py # Punto de entrada de la aplicación
├── test # Código de pruebas
│   ├── __init__.py
│   └── test_main.py # Métodos de prueba de servicio de scores
├── .env.template # Plantilla de las variables de entorno utilizadas
├── Dockerfile # Archivo para construcción de la imagen docker
├── README.md # Documentación del servicio de gestión de scores
├── requirements.txt # Lista de dependencias necesarias para producción
└── requirements-test.txt # Lista de dependencias necesarias para pruebas
```

## Requisitos

- Python 3.11.7-alpine
- Docker
- Postman
- Motor de base de datos SQL: PostgreSQL

## Ejecución

Puede ejecutar por medio de docker-compose, las instrucciones las encontrará en este README.

Para ejecutar esto en su máquina y no por medio de docker, siga los siguientes pasos:

### Windows

1. Luego de clonar el repositorio cambie a este directorio

```powershell
cd .\score_app\
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
uvicorn app.main:app --reload --port 3004
```

## Uso

### El API de gestión de scores expone los siguiente métodos

<details>
 <summary><code>POST</code> <code><b>/scores</b></code> <code>(Crear Puntaje)</code></summary>

#### Descripción

Crea un puntaje con los datos brindados

#### Cuerpo

> | Nombre               | Requerido | Tipo   | Descripción                                            |
> | -------------------- | --------- | ------ | -----------------------------------------------------  |
> | Id                   | si        | string | código de la oferta                                    |
> | offer                | si        | string | valor en dólares de la oferta para llevar el paquete   |
> | postId               | si        | string | Código de la publicación                               |
> | size                 | si        | string | "LARGE ó MEDIUM ó SMALL"                               |
> | bagCost              | si        | string | costo del equipaje                                     |

#### Encabezado

`Authorization: Bearer token`

#### Respuestas

> | HTTP Code   | Response                                                         |
> | ----------- | --------------------------------------------------------------   |
> | 401         | El token no es válido o está vencido.                            |
> | 403         | No hay token en la solicitud	                                   |
> | 400         | El id no cuenta con un formato valido                            |
> | 412         | Ya existe un score con ese mismo id                              |
> | 201         | Score Calculado exitosamente                                     |

</details>

<br/>

<details>
 <summary><code>GET</code> <code><b>/scores/{Id}</b></code> <code>(Obtener score por id)</code></summary>

#### Descripción

Retorna el score que corresponden a los parámetros de búsqueda. Solo un usuario autorizado puede realizar esta operación.

#### Parámetros

> | Método      |  GET                           |
> | Ruta        |  /scores/{Id}                  |
> | Parámetros  |  Id: id de la oferta           |

#### Encabezado

`Authorization: Bearer token`

#### Respuestas

> | HTTP Code   | Response                                                         |
> | ----------- | --------------------------------------------------------------   |
> | 401         | El token no es válido o está vencido.                            |
> | 403         | No hay token en la solicitud	                                   |
> | 400         | El id no cuenta con un formato valido                            |
> | 200         | <pre lang="json">{&#13; "id":"7b62bb99-af05-42ba-969d-91befe16061a",&#13; "offer":514.0,"postId":"a462bf1f-6499-41a1-9981-ee59519f1408",&#13; "size":"SMALL", &#13;"bagCost":244.0, &#13;  "profit":453.0 &#13;}</pre>   |

</details>

<br/>

<details>
 <summary><code>GET</code> <code><b>/scores</b></code> <code>(Consultar los puntajes)</code></summary>

#### Descripción

Retorna los puntajes, solo un usuario autorizado puede realizar esta operación.

#### Parametros

> | Parametro   | Tipo     | Descripción                                                      |
> | ----------- | -------- | --------------------------------------------------------------   |
> | postId      | String   | (Opcional) Busca los puntajes por idde publicación, solo si es proporcionado en la petición. En el caso de que ninguno esté presente se devolverá la lista de datos sin filtrar. Es decir, todas las publicaciones.       |
> | Owner       | String   | (Opcional) dueño de la publicación. Se reciben ids o el valor `me` que indica al usuario del token. En el caso de que ninguno esté presente se devolverá la lista de datos sin filtrar. Es decir, todas las publicaciones. |


#### Encabezado

`Authorization: Bearer token`

#### Respuestas


> | HTTP Code   | Response                                                         |
> | ----------- | --------------------------------------------------------------   |
> | 401         | El token no es válido o está vencido.                            |
> | 403         | No hay token en la solicitud	                                   |
> | 400         | El cuerpo de la petición no cuenta con un formato valido o no existe  |
> | 200         | <pre lang="json">[{&#13; "id":"7b62bb99-af05-42ba-969d-91befe16061a",&#13; "offer":514.0,"postId":"a462bf1f-6499-41a1-9981-ee59519f1408",&#13; "size":"SMALL", &#13;"bagCost":244.0, &#13;  "profit":453.0 &#13;}]</pre>   |

</details>

<br/>

<details>
 <summary><code>GET</code> <code><b>/scores/ping</b></code> <code>(Consultar salud del servicio)</code></summary>

#### Descripción

Usado para verificar el estado del servicio.

#### Respuesta

> | http code | content-type | response |
> | --------- | ------------ | -------- |
> | `200`     | `text/plain` | `pong`   |

## </details>

<br/>

<details>
 <summary><code>POST</code> <code><b>/scores/reset</b></code> <code>(Restablecer base de datos)</code></summary>

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
pip install -r requirements-test.txt
```

Puede establecer un porcentaje mínimo de cobertura de código y ejecutar las pruebas con las siguientes instrucciones (con y sin reporte HTML):

```
pytest --cov-fail-under=70 --cov=app
pytest --cov-fail-under=70 --cov=app --cov-report=html
```


## Autor

Alejandra Niño Gómez <ma.ninog12@uniandes.edu.co>
