# 📱 API de Gestión de Dispositivos

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

API para la gestión de dispositivos tecnológicos, desarrollada con **FastAPI**, **SQLAlchemy** y **PostgreSQL**.

## Características

- CRUD completo de dispositivos (crear, consultar, actualizar y eliminar).
- Gestión de usuarios con administración de cuentas.
- Autenticación y autorización mediante JWT con control de acceso basado en roles y permisos.
- Registro de auditoría para el seguimiento de acciones realizadas sobre los dispositivos.
- Validación de datos utilizando Pydantic.
- Documentación interactiva de la API generada automáticamente con Swagger/OpenAPI.
- Migraciones de base de datos administradas con Alembic.
- Seeds de datos iniciales para facilitar la configuración del entorno.
- Pruebas unitarias para los servicios críticos de la aplicación.
- CI/CD con GitHub Actions para ejecutar pruebas automáticamente y publicar la imagen Docker en Docker Hub.

## Tecnologías utilizadas

| Categoría | Tecnologías |
|-----------|-------------|
| Lenguaje | Python 3.10+ |
| Framework | FastAPI |
| Base de datos | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Validación | Pydantic |
| Migraciones | Alembic |
| Autenticación | JWT |
| Testing | Pytest |
| Contenedores | Docker, Docker Compose |
| CI/CD | GitHub Actions |

## Arquitectura del proyecto

El proyecto sigue una arquitectura modular organizada por módulos de dominio.

```text
fastapi-device-manager/
├── .github/
│   └── workflows/           # Pipelines de CI/CD con GitHub Actions
├── app/
│   ├── api/
│   │   └── v1/              # Módulos de la API (auth, users, devices, roles, etc.)
│   ├── core/                # Configuración de la aplicación (DB, seguridad, dependencias)
│   ├── models/              # Modelos de SQLAlchemy
│   ├── seeds/               # Scripts para datos iniciales
│   ├── utils/               # Funciones auxiliares compartidas
│   └── main.py              # Punto de entrada de la aplicación
├── alembic/                 # Migraciones de la base de datos
├── tests/
│   └── services/            # Pruebas unitarias de la capa de servicios
├── docker-compose.yml       # Levanta la API y PostgreSQL para desarrollo local
├── Dockerfile               # Imagen Docker de la aplicación
├── .env.template            # Variables de entorno de ejemplo
├── .gitignore
├── requirements.txt
└── README.md
```

## Arquitectura interna

La aplicación está organizada por **módulos de dominio**, donde cada módulo encapsula su propia lógica de negocio y mantiene una clara separación de responsabilidades.

El flujo de una solicitud es el siguiente:

```text
Cliente
   │
   ▼
FastAPI Router
   │
   ▼
Service
(Lógica de negocio)
   │
   ▼
Repository
(Acceso a datos)
   │
   ▼
SQLAlchemy ORM
   │
   ▼
PostgreSQL
```

Cada módulo implementa los siguientes componentes:

| Componente | Responsabilidad |
|------------|-----------------|
| **router.py** | Expone los endpoints de la API, valida las solicitudes y delega la lógica al servicio correspondiente. |
| **service.py** | Implementa la lógica de negocio y coordina las operaciones de la aplicación. |
| **repository.py** | Gestiona el acceso a la base de datos mediante SQLAlchemy. |
| **schemas.py** | Define los modelos de entrada y salida utilizando Pydantic para la validación y serialización de datos. |

## Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Docker
- Docker Compose

## Configuración e instalación

Sigue estos pasos para levantar el entorno de desarrollo localmente.

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd fastapi-device-manager
```

### 2. Configurar las variables de entorno

Copia el archivo de plantilla y crea tu archivo `.env`:

```bash
cp .env.template .env
```

Completa las siguientes variables:

| Variable | Descripción | Ejemplo |
|----------|-------------|----------|
| `DATABASE_URL` | Cadena de conexión a PostgreSQL. Si utilizas Docker Compose, el host debe ser `db`. | `postgresql+psycopg://test:test@db:5432/postgres` |
| `SECRET_KEY` | Clave utilizada para firmar y validar los tokens JWT. | `my-super-secret-key` |
| `ALGORITHM` | Algoritmo de firma de los tokens JWT. | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de expiración del token de acceso, en minutos. | `30` |
| `DEFAULT_ADMIN_EMAIL` | Correo electrónico del administrador inicial. | `admin@example.com` |
| `DEFAULT_ADMIN_FIRSTNAME` | Nombre del administrador inicial. | `Admin` |
| `DEFAULT_ADMIN_LASTNAME` | Apellido del administrador inicial. | `User` |
| `DEFAULT_ADMIN_PASSWORD` | Contraseña del administrador inicial. | `Admin123!` |

> **Nota:** Si ejecutas el proyecto mediante Docker Compose, `DATABASE_URL` debe utilizar el host `db`, ya que corresponde al nombre del servicio de PostgreSQL definido en `docker-compose.yml`. Si ejecutas la API directamente desde tu máquina, deberás cambiar el host por `localhost` (o el correspondiente a tu instalación de PostgreSQL).

### 3. Levantar el entorno

```bash
docker compose up -d
```

> **Nota:** Si realizas cambios en el `Dockerfile` o en las dependencias (`requirements.txt`), reconstruye la imagen con:
>
> ```bash
> docker compose up -d --build
> ```

### 4. Ejecutar las migraciones

```bash
docker compose exec web alembic upgrade head
```

### 5. Ejecutar los seeds

Inserta los datos iniciales necesarios, incluyendo el usuario administrador.

```bash
docker compose exec web python -m app.seeds
```

## Acceso a la aplicación

Una vez iniciados los servicios, la aplicación estará disponible en:

- **API:** http://127.0.0.1:8000
- **Swagger UI:** http://127.0.0.1:8000/docs
