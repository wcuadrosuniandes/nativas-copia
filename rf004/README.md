# Creación de ofertas

Servicio para la creación de ofertas.

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
│   │   └── entities.py # Define la entidad de usuario utilizando SQLModel, así como entidades FastAPI Request/Response relacionadas.
│   ├── routers # Contiene las rutas del servicio
│   │   ├── __init__.py
│   │   └── rf004.py # Contiene los métodos expuestos por la ruta /users
│   ├── __init__.py
│   ├── dependencies.py # Dependencias, pricipalmente instancia de base de datos
│   └── main.py # Punto de entrada de la aplicación
├── test # Código de pruebas
│   ├── __init__.py
│   └── conftest.py # Métodos de prueba de servicio de usuarios
│   └── test_main.py # Métodos de prueba de servicio de usuarios
├── .env.template # Plantilla de las variables de entorno utilizadas
├── .env.test # Plantilla de las variables de entorno utilizadas
├── Dockerfile # Archivo para construcción de la imagen docker
├── PipFile # Lista de dependencias necesarias para producción
├── Pipfile.lock # Lista de dependencias necesarias para pruebas
└── README.md # Documentación del servicio de gestión de usuarios
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
uvicorn app.main:app --reload --port 3006
```

### SO basados en Unix

1. Luego de clonar el repositorio cambie a este directorio

```bash
cd rf004
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
uvicorn app.main:app --reload --port 3006
```

## Uso

### El microservicio RF004

<details>
 <summary><code>POST</code> <code><b>/rf004/posts/{id}/offers</b></code> <code>(Crear Oferta)</code></summary>

#### Descripción

Como usuario deseo ofertar sobre alguna publicación de otro usuario para poder contratar un servicio.

#### Cuerpo

> | Nombre      | Requerido | Tipo    | Descripción                                        |
> | ----------- | --------- | ------- | -------------------------------------------------- |
> | description | si        | string  | descripción de la oferta                           |
> | size        | si        | string  | tamaño del paquete puede ser SMALL, MEDIUM o LARGE |
> | fragile     | si        | boolean | indica si el paquete a llevar es frágil            |
> | offer       | si        | int     | Valor de la oferta                                 |

#### Respuestas

<table>
<tr>
<td> Código </td> <td> Descripción </td> <td> Cuerpo </td>
</tr>
<tr>
<td> 400 </td> <td> En el caso que alguno de los campos no esté presente en la solicitud.</td> <td> N/A </td>
</tr>
<tr>
<td> 401 </td> <td> El token no es válido o está vencido.</td> <td> N/A </td>
</tr>
<tr>
<td> 403 </td> <td> El token no está en la solicitud.</td> <td> N/A </td>
</tr>
<tr>
<td> 404 </td> <td> La publicación a la que se quiere asociar la oferta no existe.</td> <td> N/A </td>
</tr>
<tr>
<td> 412 </td> <td> La publicación es del mismo usuario y no se puede ofertar por ella.</td> <td> N/A </td>
</tr>
<tr>
<td> 412 </td> <td> La publicación ya está expirada y no se reciben más ofertas por ella.</td> <td> N/A </td>
</tr>
<tr>
</tr>
<tr>
<td> 201 </td>
<td> Si la creación de la oferta es exitosa. La utilidad de la oferta queda almacenada en la base de datos del servicio de utilidad.</td>
<td>

```json
{
    "data": {
       "id": id de la oferta,
       "userId": id del usuario dueño de la oferta,
       "createdAt": fecha de creación de la oferta,
       "postId": id de la publicación
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

Oscar Buitrago <o.buitragov@uniandes.edu.co>
