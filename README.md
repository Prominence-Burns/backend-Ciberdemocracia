# Ciberdemocracia backend 🗳️

Sistema de auditoría electoral con inteligencia artificial para la clasificación, validación y trazabilidad de boletas y actas del PREP.

---

## Descripción

CIberdemocracia es una API REST construida con FastAPI y SQLite que permite:

- Registrar casillas electorales con metadatos oficiales INE
- Procesar boletas escaneadas con clasificación por IA y validación humana
- Gestionar actas PREP con extracción automática de texto
- Detectar y registrar inconsistencias en el proceso electoral
- Mantener una bitácora inmutable de eventos del sistema
- Consultar resultados agregados por casilla y partido

---

## Tecnologías

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.11 | Lenguaje base |
| FastAPI | 0.136.1 | Framework API REST |
| SQLAlchemy | 2.0.49 | ORM |
| SQLite | — | Base de datos |
| Alembic | 1.18.4 | Migraciones |
| Pydantic | 2.13.4 | Validación de datos |
| Uvicorn | 0.47.0 | Servidor ASGI |

---

## Estructura del proyecto

```
CIberdemocracia/
├── app/
│   ├── __init__.py
│   ├── main.py               ← punto de entrada
│   ├── database.py           ← conexión a SQLite
│   ├── models/               ← tablas de la base de datos
│   │   ├── user.py
│   │   ├── polling_station.py
│   │   ├── ballot.py
│   │   ├── tally_sheet.py
│   │   ├── event.py
│   │   ├── inconsistency.py
│   │   └── result.py
│   ├── schemas/              ← validación Pydantic
│   │   ├── user.py
│   │   ├── polling_station.py
│   │   ├── ballot.py
│   │   ├── tally_sheet.py
│   │   ├── event.py
│   │   ├── inconsistency.py
│   │   └── result.py
│   └── routers/              ← endpoints CRUD
│       ├── users.py
│       ├── polling_stations.py
│       ├── ballots.py
│       ├── tally_sheets.py
│       ├── events.py
│       ├── inconsistencies.py
│       └── results.py
├── alembic/                  ← migraciones
├── alembic.ini
├── requirements.txt
└── .env
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Prominence-Burns/backend-Ciberdemocracia.git
cd backend-Ciberdemocracia
```

### 2. Crear y activar entorno virtual

```bash
conda create -n ciberdemocracia python=3.11
conda activate ciberdemocracia
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```
DATABASE_URL=sqlite:///./electoral.db
```

### 5. Crear la base de datos

```bash
alembic upgrade head
```

### 6. Levantar el servidor

```bash
uvicorn app.main:app --reload
```

---

## Uso

Una vez levantado el servidor, accede a la documentación interactiva:

| URL | Descripción |
|---|---|
| `http://127.0.0.1:8000/docs` | Swagger UI — prueba los endpoints |
| `http://127.0.0.1:8000/redoc` | ReDoc — documentación alternativa |
| `http://127.0.0.1:8000/` | Health check |

---

## Endpoints principales

### Casillas (`/polling-stations`)
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/polling-stations/` | Listar todas las casillas |
| POST | `/polling-stations/` | Registrar casilla |
| GET | `/polling-stations/{id}` | Consultar casilla |
| DELETE | `/polling-stations/{id}` | Eliminar casilla |

### Boletas (`/ballots`)
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/ballots/` | Listar boletas |
| POST | `/ballots/` | Registrar boleta escaneada |
| GET | `/ballots/{id}` | Consultar boleta |
| DELETE | `/ballots/{id}` | Eliminar boleta |

### Eventos (`/events`)
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/events/` | Listar eventos del sistema |
| POST | `/events/` | Registrar evento |
| GET | `/events/{id}` | Consultar evento |

### Otros endpoints
- `/users/` — Gestión de usuarios y roles
- `/tally-sheets/` — Actas PREP
- `/inconsistencies/` — Inconsistencias detectadas
- `/results/` — Resultados por casilla y partido

---

## Modelo de datos

### Entidades principales

```
polling_stations    ← casillas electorales
    └── users       ← funcionarios asignados
    └── ballots     ← boletas procesadas
    └── tally_sheets← actas PREP
    └── results     ← resultados agregados

ballots
    └── inconsistencies ← anomalías detectadas

events              ← bitácora del sistema (trazabilidad)
```

### Tipos de eventos registrados

| Evento | Descripción |
|---|---|
| `ballot_scanned` | Boleta escaneada |
| `vote_detected` | Voto clasificado por IA |
| `inconsistency_detected` | Anomalía encontrada |
| `manual_override` | Corrección humana |
| `results_submitted` | Resultados enviados |
| `dashboard_updated` | Dashboard actualizado |

---

## Integración con sistema de visión

La API acepta el esquema oficial INE (`urn:ine:aecc:casilla:v1`) con los siguientes bloques:

- `metadatos` → `polling_stations`
- `bloque_1` → `tally_sheets` (conteos de boletas)
- `bloque_2.resultados` → `results` (votos por partido/coalición)
- `consistencia` → `inconsistencies`
- `hash_boletas` → `events.hash`

---

## Contribución

1. Haz fork del repositorio
2. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. Haz commit de tus cambios: `git commit -m "Add: nueva funcionalidad"`
4. Sube la rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## Licencia

Este proyecto es parte de una iniciativa académica de la Universidad Autónoma de Ciudad Juárez (UACJ).

---

## Contacto

Proyecto desarrollado en la UACJ — Ciudad Juárez, Chihuahua, México.