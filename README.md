# 📱 API de Gestión de Dispositivos

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

API para la gestión de dispositivos tecnologicos, desarrollada con **FastAPI**, **SQLAlchemy** y **PostgreSQL**.

## Caracteristicas
- CRUD de dispositivos
- Gestión de usuarios
- Auditoria de acciones sobre dispositivos
- Autenticación mediante JWT
- Roles y permisos
- Validación de datos con Pydantic
- Documentación automática con Swagger
- Seeds para datos iniciales

## Arquitectura del proyecto


El proyecto sigue una estructura limpia y modular organizada por capas de dominio:
```text
fastapi-device-manager/
├── app/
│   ├── api/                 # Controladores y Endpoints de la API
│   │   └── v1/              # Versión 1 de la API (auth, devices, roles, etc.)
│   ├── core/                # Configuraciones core (Base de datos, Middlewares, Seguridad)
│   ├── models/              # Modelos de SQLAlchemy (Base de datos)
│   ├── seeds/               # Scripts para inserción de datos iniciales (semillas)
│   ├── utils/               # Utilidades y funciones auxiliares (contraseñas, etc.)
│   └── main.py              # Punto de entrada de la aplicación 
├── docker-compose.yml       # Orquestación del contenedor de la base de datos PostgreSQL
├── .env.template            # Plantilla para variables de entorno
└── requeriments.txt         # Dependencias del proyecto
```

## Requisitos previos
Asegúrate de tener instalados los siguientes componentes en tu sistema:
- Python 3.10 o superior
- Docker y Docker Compose

## Configuracion e instalacion
Sigue estos pasos para levantar el entorno de desarrollo localmente:
### 1. Clonar el repositorio y acceder al proyecto
```bash
git clone <url-del-repositorio>
cd fastapi-device-manager
```
### 2. Configurar las variables de entorno
Copia el archivo de plantilla `.env.template` como `.env`:
```bash
cp .env.template .env
```
Abre el archivo `.env` y define los valores necesarios, por ejemplo:
*   `DATABASE_URL=postgresql+psycopg://test:test@localhost:5432/postgres`
*   `SECRET_KEY` (Clave secreta segura para firmar los tokens JWT)
*   Datos por defecto del administrador (`DEFAULT_ADMIN_EMAIL`, `DEFAULT_ADMIN_PASSWORD`, etc.)
### 3. Levantar la Base de Datos (PostgreSQL) con Docker
Inicia el contenedor de la base de datos PostgreSQL:
```bash
docker-compose up -d
```
### 4. Crear el Entorno Virtual e Instalar Dependencias
Crea y activa un entorno virtual de Python, luego instala las dependencias:
```bash
# Crear entorno virtual
python -m venv .venv
# Activar entorno virtual
# En Windows (PowerShell):
.venv\Scripts\Activate.ps1
# En Linux/macOS:
source .venv/bin/activate
# Instalar dependencias
pip install -r requirements.txt
```
### 5. Ejecutar las Semillas (*Seeds*)
Inserta los datos iniciales obligatorios y el usuario administrador en la base de datos:
```bash
python -m seeds
```

## Ejecucion de la aplicación
Para iniciar el servidor de desarrollo local con recarga automática:
```bash
uvicorn app.main:app --reload
```
El servidor estará corriendo en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Documentacion
La documentación Swagger para endpoints públicos (auth, roles, usuarios) se encuentra disponible en:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
