# Ciberdemocracia — Backend API

> Sistema de auditoría electoral con Inteligencia Artificial para el escrutinio y cómputo de casillas electorales del estado de Chihuahua.

Desarrollado en el marco del **Hackathon Ciberdemocracia**, organizado por el **Instituto Estatal Electoral de Chihuahua (IEE Chihuahua)** y el **Tecnológico de Monterrey**.

---

## Descripción

Backend REST API que recibe, procesa y almacena los datos generados por el sistema de visión artificial de casillas electorales. Implementa el esquema AECC (`urn:ine:aecc:casilla:v1`) para el Acta de Escrutinio y Cómputo de Casilla, incluyendo:

- Registro de casillas electorales
- Procesamiento de boletas con clasificación por IA
- Registro de actas PREP con criterios de consistencia
- Trazabilidad de eventos y auditoría
- Detección y resolución de inconsistencias
- Resultados agregados por partido o coalición

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
│   ├── main.py               ← punto de entrada
│   ├── database.py           ← conexión SQLite
│   ├── models/               ← tablas de la BD
│   │   ├── casilla.py
│   │   ├── usuario.py
│   │   ├── boleta.py
│   │   ├── acta.py
│   │   ├── evento.py
│   │   ├── inconsistencia.py
│   │   └── resultado.py
│   ├── schemas/              ← validación Pydantic
│   │   ├── casilla.py
│   │   ├── usuario.py
│   │   ├── boleta.py
│   │   ├── acta.py
│   │   ├── evento.py
│   │   ├── inconsistencia.py
│   │   └── resultado.py
│   └── routers/              ← endpoints REST
│       ├── casillas.py
│       ├── usuarios.py
│       ├── boletas.py
│       ├── actas.py
│       ├── eventos.py
│       ├── inconsistencias.py
│       └── resultados.py
├── alembic/                  ← migraciones
├── requirements.txt
└── .env
```

---

## Tablas de la base de datos

| Tabla | Descripción |
|---|---|
| `casillas` | Metadatos de cada casilla electoral |
| `usuarios` | Funcionarios, auditores y administradores |
| `boletas` | Boletas procesadas por el sistema de visión |
| `actas` | Actas AECC con bloques de control y consistencia |
| `eventos` | Registro de auditoría de todas las acciones |
| `inconsistencias` | Alertas y resoluciones de inconsistencias |
| `resultados` | Votos por partido o coalición por casilla |

---

## Mapeo JSON AECC → Base de datos

El sistema recibe JSONs conformes al schema `urn:ine:aecc:casilla:v1`. El mapeo entre claves del JSON y columnas de la BD es el siguiente:

### `metadatos` → tabla `casillas`

| JSON | Columna BD |
|---|---|
| `casilla_id` | `casilla_id` |
| `entidad_federativa` | `entidad_federativa` |
| `municipio_o_delegacion` | `municipio_o_delegacion` |
| `distrito` | `distrito` |
| `seccion` | `seccion` |
| `tipo_casilla` | `tipo_casilla` |
| `tipo_eleccion` | `tipo_eleccion` |
| `proceso_electoral` | `proceso_electoral` |

### `bloque_1` → tabla `actas`

| JSON | Columna BD |
|---|---|
| `boletas_recibidas` | `boletas_recibidas` |
| `BS` | `boletas_sobrantes` |
| `PV` | `personas_votaron` |
| `RPPV` | `rep_partido_fuera_lista` |
| `SV` | `boletas_en_urna` |
| `BSU` | `boletas_contadas` |

### `bloque_2` → tabla `actas` + tabla `resultados`

| JSON | Columna BD | Tabla |
|---|---|---|
| `CNR` | `candidatos_no_registrados` | `actas` |
| `VN` | `votos_nulos` | `actas` |
| `RV` | `total_votos` | `actas` |
| `resultados[].partido_o_coalicion` | `partido_o_coalicion` | `resultados` |
| `resultados[].id` | `partido_id` | `resultados` |
| `resultados[].votos` | `votos` | `resultados` |
| `resultados[].es_coalicion` | `es_coalicion` | `resultados` |
| `resultados[].partidos_coalicion` | `partidos_coalicion` | `resultados` |

### `consistencia` → tabla `actas`

| JSON | Columna BD |
|---|---|
| `criterio_1_pv_rppv_sv` | `criterio_1` |
| `criterio_2_sv_bsu` | `criterio_2` |
| `criterio_3_bsu_rv` | `criterio_3` |
| `criterio_4_sum_vi_rv` | `criterio_4` |
| `acta_consistente` | `acta_consistente` |
| `tipo_error` | `tipo_error` |

### `incidentes` → tabla `actas`

| JSON | Columna BD |
|---|---|
| `se_presentaron` | `incidentes_presentes` |
| `descripcion` | `descripcion_incidentes` |
| `hojas_de_incidentes` | `hojas_incidentes` |

### Raíz del JSON → tabla `actas`

| JSON | Columna BD |
|---|---|
| `boletas_procesadas` | `boletas_procesadas` |
| `boletas_revision_humana` | `boletas_revision_humana` |
| `hash_boletas` | `hash_boletas` |

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Prominence-Burns/backend-Ciberdemocracia.git
cd backend-Ciberdemocracia

# 2. Crear entorno virtual
conda create -n ciberdemocracia python=3.11
conda activate ciberdemocracia

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# Crear archivo .env con el siguiente contenido:
# DATABASE_URL=sqlite:///./electoral.db

# 5. Crear base de datos
alembic upgrade head

# 6. Levantar servidor
uvicorn app.main:app --reload
```

---

## Documentación de la API

Una vez levantado el servidor, accede a:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### Endpoints disponibles

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/casillas/` | Registrar casilla |
| GET | `/casillas/` | Listar casillas |
| GET | `/casillas/{id}` | Obtener casilla |
| POST | `/actas/` | Registrar acta AECC |
| GET | `/actas/` | Listar actas |
| POST | `/boletas/` | Registrar boleta |
| GET | `/boletas/` | Listar boletas |
| POST | `/resultados/` | Registrar resultado |
| GET | `/resultados/` | Listar resultados |
| POST | `/eventos/` | Registrar evento |
| GET | `/eventos/` | Listar eventos |
| POST | `/inconsistencias/` | Registrar inconsistencia |
| GET | `/inconsistencias/` | Listar inconsistencias |
| POST | `/usuarios/` | Registrar usuario |
| GET | `/usuarios/` | Listar usuarios |

---

## Licencia

Este proyecto fue desarrollado con fines académicos y de innovación cívica en el marco del **Hackathon CIberdemocracia 2024**, organizado por:

- **Instituto Estatal Electoral de Chihuahua (IEE Chihuahua)**
- **Tecnológico de Monterrey**

El uso del código fuente está permitido exclusivamente para fines educativos, de investigación y de mejora de los procesos electorales del estado de Chihuahua. Queda prohibida su reproducción o uso comercial sin autorización expresa de los organizadores del hackathon y del equipo desarrollador.

© 2024 IEE Chihuahua — Hackathon CIberdemocracia. Todos los derechos reservados.

---

## Equipo

| GitHub | Perfil |
|---|---|
| [@DeysChain](https://github.com/DeysChain) | Desarrollador |
| [@YopiYuli](https://github.com/YopiYuli) | Desarrollador |
| [@jedesvaz](https://github.com/jedesvaz) | Desarrollador |
