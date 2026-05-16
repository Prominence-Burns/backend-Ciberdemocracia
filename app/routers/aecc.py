from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.casilla import Casilla
from app.models.acta import Acta
from app.models.resultado import Resultado
from app.models.evento import Evento
from pydantic import BaseModel
from typing import Optional, List
import uuid

router = APIRouter(prefix="/aecc", tags=["AECC"])

# ── Schema de confirmación ───────────────────────────────────────────────────
class ConfirmacionAecc(BaseModel):
    acta_id: str
    confirmado: bool
    usuario_id: Optional[str] = None
    notas: Optional[str] = None

# ── Schemas internos para recibir el JSON completo ──────────────────────────

class Metadatos(BaseModel):
    casilla_id: str
    entidad_federativa: str
    municipio_o_delegacion: str
    distrito: str
    seccion: str
    tipo_casilla: str
    tipo_eleccion: str
    proceso_electoral: str

class Bloque1(BaseModel):
    boletas_recibidas: int
    BS: int
    PV: int
    RPPV: int
    SV: int
    BSU: int

class ResultadoPartido(BaseModel):
    partido_o_coalicion: str
    id: str
    es_coalicion: bool
    partidos_coalicion: Optional[List[str]] = None
    votos: int

class Bloque2(BaseModel):
    resultados: List[ResultadoPartido]
    CNR: int
    VN: int
    RV: int

class Consistencia(BaseModel):
    criterio_1_pv_rppv_sv: bool
    criterio_2_sv_bsu: bool
    criterio_3_bsu_rv: bool
    criterio_4_sum_vi_rv: bool
    acta_consistente: bool
    tipo_error: str

class Incidentes(BaseModel):
    se_presentaron: bool
    descripcion: Optional[str] = None
    hojas_de_incidentes: int

class JSONAecc(BaseModel):
    metadatos: Metadatos
    bloque_1: Bloque1
    bloque_2: Bloque2
    consistencia: Consistencia
    incidentes: Incidentes
    boletas_procesadas: int
    boletas_revision_humana: int
    hash_boletas: str


# ── Endpoint principal ───────────────────────────────────────────────────────

@router.post("/casilla")
def recibir_aecc(payload: JSONAecc, db: Session = Depends(get_db)):
    """
    Recibe el JSON AECC completo del sistema de visión
    y lo distribuye en casillas, actas y resultados.
    """

    # ── 1. Busca o crea la casilla ───────────────────────────────────────────
    casilla = db.query(Casilla).filter(
        Casilla.casilla_id == payload.metadatos.casilla_id
    ).first()

    if not casilla:
        casilla = Casilla(
            casilla_id=payload.metadatos.casilla_id,
            entidad_federativa=payload.metadatos.entidad_federativa,
            municipio_o_delegacion=payload.metadatos.municipio_o_delegacion,
            distrito=payload.metadatos.distrito,
            seccion=payload.metadatos.seccion,
            tipo_casilla=payload.metadatos.tipo_casilla,
            tipo_eleccion=payload.metadatos.tipo_eleccion,
            proceso_electoral=payload.metadatos.proceso_electoral
        )
        db.add(casilla)
        db.flush()  # genera el id sin hacer commit aún

    # ── 2. Crea el acta ──────────────────────────────────────────────────────
    acta_existente = db.query(Acta).filter(
        Acta.casilla_id == casilla.id
    ).first()

    if acta_existente:
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe un acta para la casilla {payload.metadatos.casilla_id}"
        )

    acta = Acta(
        casilla_id=casilla.id,

        # bloque_1
        boletas_recibidas=payload.bloque_1.boletas_recibidas,
        BS=payload.bloque_1.BS,
        PV=payload.bloque_1.PV,
        RPPV=payload.bloque_1.RPPV,
        SV=payload.bloque_1.SV,
        BSU=payload.bloque_1.BSU,

        # bloque_2
        CNR=payload.bloque_2.CNR,
        VN=payload.bloque_2.VN,
        RV=payload.bloque_2.RV,

        # consistencia
        criterio_1_pv_rppv_sv=payload.consistencia.criterio_1_pv_rppv_sv,
        criterio_2_sv_bsu=payload.consistencia.criterio_2_sv_bsu,
        criterio_3_bsu_rv=payload.consistencia.criterio_3_bsu_rv,
        criterio_4_sum_vi_rv=payload.consistencia.criterio_4_sum_vi_rv,
        acta_consistente=payload.consistencia.acta_consistente,
        tipo_error=payload.consistencia.tipo_error,

        # incidentes
        se_presentaron=payload.incidentes.se_presentaron,
        descripcion=payload.incidentes.descripcion,
        hojas_de_incidentes=payload.incidentes.hojas_de_incidentes,

        # raíz
        boletas_procesadas=payload.boletas_procesadas,
        boletas_revision_humana=payload.boletas_revision_humana,
        hash_boletas=payload.hash_boletas,

        validation_status="pendiente" if not payload.consistencia.acta_consistente else "consistente"
    )
    db.add(acta)
    db.flush()  # genera el id del acta sin hacer commit aún

    # ── 3. Crea un resultado por cada partido ────────────────────────────────
    for r in payload.bloque_2.resultados:
        resultado = Resultado(
            acta_id=acta.id,
            partido_o_coalicion=r.partido_o_coalicion,
            partido_id=r.id,
            votos=r.votos,
            es_coalicion=r.es_coalicion,
            partidos_coalicion=r.partidos_coalicion
        )
        db.add(resultado)

    # ── 4. Registra el evento de auditoría ───────────────────────────────────
    evento = Evento(
        entidad_tipo="acta",
        entidad_id=acta.id,
        tipo_evento="aecc_recibido",
        detalles={
            "casilla_id": payload.metadatos.casilla_id,
            "acta_consistente": payload.consistencia.acta_consistente,
            "total_votos": payload.bloque_2.RV,
            "hash_boletas": payload.hash_boletas
        }
    )
    db.add(evento)

    # ── 5. Commit único — todo o nada ────────────────────────────────────────
    db.commit()

    return {
        "mensaje": "AECC procesado correctamente",
        "casilla_id": casilla.id,
        "acta_id": acta.id,
        "acta_consistente": payload.consistencia.acta_consistente,
        "partidos_guardados": len(payload.bloque_2.resultados),
        "validation_status": acta.validation_status
    }

# ── Schemas para confirmación ────────────────────────────────────────────────

class ConfirmacionAecc(BaseModel):
    acta_id: str
    confirmado: bool
    usuario_id: Optional[str] = None
    notas: Optional[str] = None


# ── Endpoint de confirmación ─────────────────────────────────────────────────

@router.post("/confirmar")
def confirmar_aecc(payload: ConfirmacionAecc, db: Session = Depends(get_db)):
    """
    Recibe la confirmación de la app sobre los datos del acta.
    Actualiza el validation_status y registra el evento de auditoría.
    """

    # 1. Busca el acta
    acta = db.query(Acta).filter(Acta.id == payload.acta_id).first()

    if not acta:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el acta con id {payload.acta_id}"
        )

    # 2. Actualiza el status según la confirmación
    if payload.confirmado:
        acta.validation_status = "confirmado"
    else:
        acta.validation_status = "rechazado"

    # 3. Registra el evento de auditoría
    evento = Evento(
        entidad_tipo="acta",
        entidad_id=acta.id,
        tipo_evento="acta_confirmada" if payload.confirmado else "acta_rechazada",
        usuario_id=payload.usuario_id,
        detalles={
            "acta_id": payload.acta_id,
            "confirmado": payload.confirmado,
            "notas": payload.notas
        }
    )
    db.add(evento)
    db.commit()

    return {
        "mensaje": "Confirmación registrada correctamente",
        "acta_id": acta.id,
        "validation_status": acta.validation_status,
        "confirmado": payload.confirmado
    }