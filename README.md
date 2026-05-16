# CIberdemocracia — Backend API

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
- Autenticación de funcionarios por clave de elector

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
| Passlib | — | Encriptación de contraseñas |
| httpx | 0.27.x | Cliente HTTP async |
| python-multipart | — | Recepción de archivos |

---

## Estructura del proyecto

```
CIberdemocracia/
├── app/
│   ├── main.py               ← punto de entrada, registra todos los routers
│   ├── database.py           ← conexión SQLite y sesión de BD
│   ├── models/               ← definición de tablas
│   │   ├── __init__.py
│   │   ├── casilla.py
│   │   ├── usuario.py
│   │   ├── boleta.py
│   │   ├── acta.py
│   │   ├── evento.py
│   │   ├── inconsistencia.py
│   │   └── resultado.py
│   ├── schemas/              ← validación Pydantic (entrada/salida)
│   │   ├── __init__.py
│   │   ├── casilla.py
│   │   ├── usuario.py
│   │   ├── boleta.py
│   │   ├── acta.py
│   │   ├── evento.py
│   │   ├── inconsistencia.py
│   │   └── resultado.py
│   ├── routers/              ← endpoints REST
│   │   ├── __init__.py
│   │   ├── casillas.py
│   │   ├── usuarios.py
│   │   ├── boletas.py
│   │   ├── actas.py
│   │   ├── eventos.py
│   │   ├── inconsistencias.py
│   │   ├── resultados.py
│   │   ├── vision.py         ← recibe foto y reenvía a sistema de visión
│   │   ├── aecc.py           ← recibe JSON AECC completo y lo distribuye
│   │   └── auth.py           ← registro y login de usuarios
│   └── utils/
│       └── security.py       ← encriptación y verificación de contraseñas
├── alembic/                  ← migraciones de BD
├── requirements.txt
└── .env
```

---

## Base de datos

### Tabla `casillas`
Representa una casilla electoral. Es la tabla raíz del sistema — todas las demás tablas apuntan a ella. Almacena los metadatos que identifican de forma única cada casilla dentro del proceso electoral.

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador interno generado automáticamente |
| `casilla_id` | TEXT | Clave única de la casilla según el sistema externo (ej: DEMO-001-001-B) |
| `entidad_federativa` | TEXT | Estado donde se ubica la casilla |
| `municipio_o_delegacion` | TEXT | Municipio o delegación donde se ubica |
| `distrito` | TEXT | Distrito electoral |
| `seccion` | TEXT | Sección electoral |
| `tipo_casilla` | TEXT | Tipo de casilla (basica, contigua, extraordinaria, especial) |
| `tipo_eleccion` | TEXT | Tipo de cargo en disputa (diputacion_mr, gubernatura, presidencia_mpal, etc.) |
| `proceso_electoral` | TEXT | Identificador del proceso electoral (ej: 2023-2024) |
| `created_at` | TIMESTAMP | Fecha y hora de registro |

---

### Tabla `usuarios`
Representa a las personas que operan el sistema en casilla. Incluye funcionarios electorales, auditores y administradores. Maneja autenticación por clave de elector y contraseña encriptada.

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador interno generado automáticamente |
| `nombre` | TEXT | Nombre completo del funcionario (opcional) |
| `clave_de_elector` | TEXT | Clave de elector única, usada como nombre de usuario para login |
| `rol` | TEXT | Rol del usuario: presidente_de_casilla, primer_escrutador, segundo_escrutador, tercer_escrutador, primer_secretario, segundo_secretario, auditor, admin |
| `password_hash` | TEXT | Contraseña encriptada con sha256_crypt |
| `casilla_id` | FK → casillas | Casilla a la que está asignado el usuario |
| `created_at` | TIMESTAMP | Fecha y hora de registro |

---

### Tabla `boletas`
Representa cada boleta individual procesada por el sistema de visión artificial. Es el nivel más granular del sistema — cada boleta física escaneada genera un registro aquí.

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador interno generado automáticamente |
| `casilla_id` | FK → casillas | Casilla a la que pertenece la boleta |
| `image_url` | TEXT | URL de la imagen de la boleta almacenada |
| `voto_detectado` | TEXT | Partido o candidato detectado por la IA (SHH, PAN, MORENA, NULO, etc.) |
| `confianza_ia` | FLOAT | Nivel de confianza de la detección (0.0 a 1.0) |
| `revision_humana` | BOOLEAN | Indica si la boleta fue revisada por un humano |
| `clasificacion_final` | TEXT | Clasificación definitiva tras revisión humana |
| `created_at` | TIMESTAMP | Fecha y hora de registro |

---

### Tabla `actas`
Es la tabla más importante del sistema. Almacena el contenido completo del Acta de Escrutinio y Cómputo de Casilla (AECC), incluyendo el control de boletas, los totales de votos, los criterios de consistencia, los incidentes y el hash de integridad.

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador interno generado automáticamente |
| `casilla_id` | FK → casillas | Casilla a la que pertenece el acta |
| `image_url` | TEXT | URL de la imagen del acta física |
| **Bloque 1 — Control de boletas** | | |
| `boletas_recibidas` | INTEGER | Total de boletas recibidas en la casilla (BR) |
| `BS` | INTEGER | Boletas sobrantes al final de la jornada |
| `PV` | INTEGER | Personas que efectivamente votaron |
| `RPPV` | INTEGER | Representantes de partido que votaron fuera de lista |
| `SV` | INTEGER | Boletas en urna (SV = PV + RPPV) |
| `BSU` | INTEGER | Boletas contadas al abrir la urna |
| **Bloque 2 — Totales** | | |
| `CNR` | INTEGER | Votos para candidatos no registrados |
| `VN` | INTEGER | Votos nulos |
| `RV` | INTEGER | Total de votos válidos contados |
| **Consistencia** | | |
| `criterio_1_pv_rppv_sv` | BOOLEAN | C1: PV + RPPV = SV |
| `criterio_2_sv_bsu` | BOOLEAN | C2: SV = BSU |
| `criterio_3_bsu_rv` | BOOLEAN | C3: BSU = RV |
| `criterio_4_sum_vi_rv` | BOOLEAN | C4: Suma de votos por partido + CNR + VN = RV |
| `acta_consistente` | BOOLEAN | True si los 4 criterios se cumplen |
| `tipo_error` | TEXT | Descripción del error si el acta no es consistente |
| **Incidentes** | | |
| `se_presentaron` | BOOLEAN | Indica si hubo incidentes durante la jornada |
| `descripcion` | TEXT | Descripción de los incidentes ocurridos |
| `hojas_de_incidentes` | INTEGER | Número de hojas de incidentes levantadas |
| **Integridad** | | |
| `boletas_procesadas` | INTEGER | Total de boletas procesadas por el sistema de visión |
| `boletas_revision_humana` | INTEGER | Boletas que requirieron revisión humana |
| `hash_boletas` | TEXT | Hash SHA-256 de integridad del conjunto de boletas |
| `validation_status` | TEXT | Estado de validación: pendiente, consistente, confirmado, rechazado |
| `created_at` | TIMESTAMP | Fecha y hora de registro |

---

### Tabla `resultados`
Almacena los votos por partido o coalición. Como el JSON AECC trae un arreglo de resultados, esta tabla genera un registro por cada partido, todos vinculados al mismo acta.

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador interno generado automáticamente |
| `acta_id` | FK → actas | Acta a la que pertenece este resultado |
| `partido_o_coalicion` | TEXT | Nombre completo del partido o coalición (ej: Sigamos Haciendo Historia) |
| `partido_id` | TEXT | Clave corta del partido (ej: SHH, PAN, MORENA, MC, FCM) |
| `votos` | INTEGER | Total de votos obtenidos |
| `es_coalicion` | BOOLEAN | Indica si es una coalición de varios partidos |
| `partidos_coalicion` | JSON | Lista de partidos que integran la coalición (ej: ["PAN","PRI","PRD"]) |
| `created_at` | TIMESTAMP | Fecha y hora de registro |

---

### Tabla `eventos`
Registro de auditoría inmutable. Cada acción relevante del sistema genera un evento. No tiene endpoint DELETE para preservar la trazabilidad completa.

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador interno generado automáticamente |
| `entidad_tipo` | TEXT | Tipo de entidad afectada (boleta, acta, casilla, resultado) |
| `entidad_id` | UUID | ID de la entidad afectada |
| `tipo_evento` | TEXT | Tipo de acción: aecc_recibido, acta_confirmada, acta_rechazada, boleta_escaneada, voto_detectado, inconsistencia_detectada, etc. |
| `usuario_id` | FK → usuarios | Usuario que generó el evento (opcional) |
| `timestamp` | TIMESTAMP | Fecha y hora exacta del evento |
| `detalles` | JSON | Información adicional del evento en formato libre |
| `hash` | TEXT | Hash de integridad del evento |

---

### Tabla `inconsistencias`
Almacena las alertas generadas cuando el sistema detecta problemas. No tiene endpoint DELETE para preservar el historial de alertas.

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador interno generado automáticamente |
| `boleta_id` | FK → boletas | Boleta que presentó el problema |
| `tipo_inconsistencia` | TEXT | Tipo de problema: baja_confianza_ia, voto_ilegible, criterio_fallido, etc. |
| `severidad` | TEXT | Nivel de gravedad: baja, media, alta |
| `resuelta` | BOOLEAN | Indica si la inconsistencia fue resuelta |
| `notas_resolucion` | TEXT | Descripción de cómo se resolvió |
| `resuelta_por` | FK → usuarios | Usuario que resolvió la inconsistencia |
| `created_at` | TIMESTAMP | Fecha y hora de registro |

---

## Mapeo JSON AECC → Base de datos

El sistema recibe JSONs conformes al schema `urn:ine:aecc:casilla:v1`. El endpoint `/aecc/casilla` distribuye automáticamente el JSON en las tablas correspondientes.

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
| `BS` | `BS` |
| `PV` | `PV` |
| `RPPV` | `RPPV` |
| `SV` | `SV` |
| `BSU` | `BSU` |

### `bloque_2` → tabla `actas` + tabla `resultados`

| JSON | Columna BD | Tabla |
|---|---|---|
| `CNR` | `CNR` | `actas` |
| `VN` | `VN` | `actas` |
| `RV` | `RV` | `actas` |
| `resultados[].partido_o_coalicion` | `partido_o_coalicion` | `resultados` |
| `resultados[].id` | `partido_id` | `resultados` |
| `resultados[].votos` | `votos` | `resultados` |
| `resultados[].es_coalicion` | `es_coalicion` | `resultados` |
| `resultados[].partidos_coalicion` | `partidos_coalicion` | `resultados` |

### `consistencia` → tabla `actas`

| JSON | Columna BD |
|---|---|
| `criterio_1_pv_rppv_sv` | `criterio_1_pv_rppv_sv` |
| `criterio_2_sv_bsu` | `criterio_2_sv_bsu` |
| `criterio_3_bsu_rv` | `criterio_3_bsu_rv` |
| `criterio_4_sum_vi_rv` | `criterio_4_sum_vi_rv` |
| `acta_consistente` | `acta_consistente` |
| `tipo_error` | `tipo_error` |

### `incidentes` → tabla `actas`

| JSON | Columna BD |
|---|---|
| `se_presentaron` | `se_presentaron` |
| `descripcion` | `descripcion` |
| `hojas_de_incidentes` | `hojas_de_incidentes` |

### Raíz del JSON → tabla `actas`

| JSON | Columna BD |
|---|---|
| `boletas_procesadas` | `boletas_procesadas` |
| `boletas_revision_humana` | `boletas_revision_humana` |
| `hash_boletas` | `hash_boletas` |

---

## Endpoints disponibles

### Autenticación
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/auth/registro` | Registrar funcionario con clave de elector y contraseña |
| POST | `/auth/login` | Validar credenciales y obtener confirmación |

### AECC — Flujo principal
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/aecc/casilla` | Recibe JSON AECC completo y distribuye en BD |
| POST | `/aecc/confirmar` | Confirma o rechaza un acta desde la app |

### Visión
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/vision/procesar-boleta` | Recibe foto desde app y la reenvía al sistema de visión |

### CRUD básico
| Método | Ruta | Descripción |
|---|---|---|
| GET/POST/DELETE | `/casillas/` | Gestión de casillas |
| GET/POST/DELETE | `/usuarios/` | Gestión de usuarios |
| GET/POST/DELETE | `/boletas/` | Gestión de boletas |
| GET/POST/DELETE | `/actas/` | Gestión de actas |
| GET/POST | `/eventos/` | Registro de eventos (sin DELETE) |
| GET/POST | `/inconsistencias/` | Registro de inconsistencias (sin DELETE) |
| GET/POST | `/resultados/` | Resultados por partido |

---

## Flujo completo del sistema

```
1. Funcionario abre la app
         ↓
2. POST /auth/login
   valida clave_de_elector + password
         ↓
3. App toma foto de boleta o acta
         ↓
4. POST /vision/procesar-boleta
   backend reenvía foto al sistema de visión
         ↓
5. Sistema de visión genera JSON AECC
         ↓
6. POST /aecc/casilla
   backend distribuye en casillas + actas + resultados + eventos
         ↓
7. Backend regresa JSON a app para revisión
         ↓
8. Funcionario confirma desde app
   POST /aecc/confirmar
         ↓
9. BD actualiza validation_status → "confirmado"
```

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
# Crear archivo .env con:
# DATABASE_URL=sqlite:///./electoral.db

# 5. Crear base de datos
alembic upgrade head

# 6. Levantar servidor
uvicorn app.main:app --reload
```

---

## Documentación interactiva

```
Swagger UI → http://127.0.0.1:8000/docs
ReDoc      → http://127.0.0.1:8000/redoc
```

---

## Licencia

Este proyecto fue desarrollado con fines académicos y de innovación cívica en el marco del **Hackathon CIberdemocracia 2026**, organizado por:

- **Instituto Estatal Electoral de Chihuahua (IEE Chihuahua)**
- **Tecnológico de Monterrey**

El uso del código fuente está permitido exclusivamente para fines educativos, de investigación y de mejora de los procesos electorales del estado de Chihuahua. Queda prohibida su reproducción o uso comercial sin autorización expresa de los organizadores del hackathon y del equipo desarrollador.


---

## Equipo

| GitHub | Perfil |
|---|---|
| [@DeysChain](https://github.com/DeysChain) | Desarrollador |
| [@YopiYuli](https://github.com/YopiYuli) | Desarrollador |
| [@jedesvaz](https://github.com/jedesvaz) | Desarrollador |
