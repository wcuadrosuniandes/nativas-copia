# Gestión de usuarios

El servicio de gestión de usuarios permite crear usuarios y validar la identidad de un usuario por medio de tokens.

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
├── app # Contiene el código principal del servicio de gestión de usuarios
│   ├── entities # Almacena las entidades del servicio
│   │   ├── __init__.py
│   │   └── user.py # Define la entidad de usuario utilizando SQLModel, así como entidades FastAPI Request/Response relacionadas.
│   ├── routers # Contiene las rutas del servicio
│   │   ├── __init__.py
│   │   └── users.py # Contiene los métodos expuestos por la ruta /users
│   ├── __init__.py
│   ├── dependencies.py # Dependencias, pricipalmente instancia de base de datos
│   └── main.py # Punto de entrada de la aplicación
├── test # Código de pruebas
│   ├── __init__.py
│   └── test_main.py # Métodos de prueba de servicio de usuarios
├── .env.template # Plantilla de las variables de entorno utilizadas
├── Dockerfile # Archivo para construcción de la imagen docker
├── README.md # Documentación del servicio de gestión de usuarios
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
cd .\user_app\
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
cd user_app
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

### El API de gestión de usuarios expone los siguiente métodos

<details>
 <summary><code>POST</code> <code><b>/users</b></code> <code>(Crear Usuario)</code></summary>

#### Descripción

Crea un usuario con los datos brindados, el nombre del usuario debe ser único, así como el correo.

#### Cuerpo

> | Nombre      | Requerido | Tipo   | Descripción                    |
> | ----------- | --------- | ------ | ------------------------------ |
> | username    | si        | string | nombre de usuario              |
> | password    | si        | string | contraseña del usuario         |
> | email       | si        | string | correo electrónico del usuario |
> | dni         | no        | string | identificación                 |
> | fullName    | no        | string | nombre completo del usuario    |
> | phoneNumber | no        | string | número de teléfono             |

#### Respuestas

> | http code | content-type       | response                                                                                                                          |
> | --------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
> | `400`     | `application/json` | Objeto con indicación de campo con error                                                                                          |
> | `412`     | `application/json` | <pre lang="json">{&#13; "detail": "Ya existe un usuario con ese nombre o correo"&#13;}</pre>                                      |
> | `201`     | `application/json` | <pre lang="json">{&#13; "id": "29c08ee4-2c42-4171-9149-3bfe0620be8e",&#13; "createdAt": "2024-02-04T06:25:35.781980" &#13;}</pre> |

</details>

<br/>

<details>
 <summary><code>PATCH</code> <code><b>/users/{id}</b></code> <code>(Actuallizar Usuario)</code></summary>

#### Descripción

Actualiza los datos de un usuario con los datos brindados, solo los valores de fullName, phoneNumber, dni, status. Todos los valores son opcionales, solo se modifican los que se reciben, los demás permanecen sin modificarse. Este endpoint será público por decisión de arquitectura.

#### Parámetros

> | Nombre | Requerido | Tipo | Descripción               |
> | ------ | --------- | ---- | ------------------------- |
> | id     | si        | uuid | identificador del usuario |

#### Cuerpo

> | Nombre      | Requerido | Tipo   | Descripción                 |
> | ----------- | --------- | ------ | --------------------------- |
> | status      | no        | string | nuevo estado del usuario    |
> | dni         | no        | string | identificación              |
> | fullName    | no        | string | nombre completo del usuario |
> | phoneNumber | no        | string | número de teléfono          |

#### Respuesta

> | http code | content-type       | response                                                                    |
> | --------- | ------------------ | --------------------------------------------------------------------------- |
> | `400`     | `application/json` | Objeto con indicación de campo con error                                    |
> | `404`     | `application/json` | <pre lang="json">{&#13; "detail": "Usuario no encontrado"&#13;}</pre>       |
> | `201`     | `application/json` | <pre lang="json">{&#13; "msg": "el usuario ha sido actualizado"&#13;}</pre> |

</details>

<br/>

<details>
 <summary><code>POST</code> <code><b>/users/auth</b></code> <code>(Generación de Token)</code></summary>

#### Descripción

Genera un nuevo Token para el usuario correspondiente al username y contraseña.

#### Cuerpo

> | Nombre   | Requerido | Tipo   | Descripción            |
> | -------- | --------- | ------ | ---------------------- |
> | username | si        | string | nombre del usuario     |
> | password | si        | string | contraseña del usuario |

#### Respuesta

> | http code | content-type       | response                                                                                                                                                                              |
> | --------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | `400`     | `application/json` | Objeto con indicación de campo con error                                                                                                                                              |
> | `404`     | `application/json` | <pre lang="json">{&#13; "detail": "Usuario / Contraseña no existe"&#13;}</pre>                                                                                                        |
> | `201`     | `application/json` | <pre lang="json">{&#13; "id": "29c08ee4-2c42-4171-9149-3bfe0620be8e",&#13; "token": "c549bc40-2629-4bd5-93d5-daaf4da24467",&#13; "expireAt": "2024-02-04T07:44:24.071696"&#13;}</pre> |

## </details>

<br/>

<details>
 <summary><code>GET</code> <code><b>/users/me</b></code> <code>(Consultar información de usuario)</code></summary>

#### Descripción

Retorna los datos del usuario al que pertenece el token.

#### Encabezados

> | Nombre        | Requerido | Tipo   | Descripción  |
> | ------------- | --------- | ------ | ------------ |
> | Authorization | si        | string | Bearer Token |

#### Respuesta

> | http code | content-type       | response                                                                                                                                                                                                                                                                                                |
> | --------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | `401`     | `application/json` | <pre lang="json">{&#13; "detail": "Acceso denegado"&#13;}</pre>                                                                                                                                                                                                                                         |
> | `403`     | `application/json` | <pre lang="json">{&#13; "detail": "Acceso denegado"&#13;}</pre>                                                                                                                                                                                                                                         |
> | `200`     | `application/json` | <pre lang="json">{&#13; "id": "e2f54f97-9f5e-4b1c-afe0-ce76294aea46",&#13; "username": "oscar1",&#13; "email": "oscar1@dominio.com",&#13; "fullName": "nombre completo del usuario",&#13; "dni": "identificación",&#13; "phoneNumber": "número de teléfono",&#13; "status": "NO_VERIFICADO"&#13;}</pre> |

## </details>

<br/>

<details>
 <summary><code>GET</code> <code><b>/users/ping</b></code> <code>(Consultar salud del servicio)</code></summary>

#### Descripción

Usado para verificar el estado del servicio.

#### Respuesta

> | http code | content-type | response |
> | --------- | ------------ | -------- |
> | `200`     | `text/plain` | `pong`   |

## </details>

<br/>

<details>
 <summary><code>POST</code> <code><b>/users/reset</b></code> <code>(Restablecer base de datos)</code></summary>

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

Oscar Buitrago <o.buitragov@uniandes.edu.co>
