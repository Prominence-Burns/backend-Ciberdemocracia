from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.utils.security import hash_password, verify_password
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Autenticación"])


# ── Schemas ──────────────────────────────────────────────────────────────────

class RegistroUsuario(BaseModel):
    clave_de_elector: str
    rol: str
    password: str
    casilla_id: Optional[str] = None

class LoginUsuario(BaseModel):
    clave_de_elector: str
    password: str

class RespuestaLogin(BaseModel):
    mensaje: str
    usuario_id: str
    clave_de_elector: str
    rol: str
    casilla_id: Optional[str]
    autenticado: bool


# ── Registro ─────────────────────────────────────────────────────────────────

@router.post("/registro")
def registrar_usuario(data: RegistroUsuario, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(
        Usuario.clave_de_elector == data.clave_de_elector
    ).first()
    if existente:
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe un usuario con la clave {data.clave_de_elector}"
        )

    usuario = Usuario(
        clave_de_elector=data.clave_de_elector,
        rol=data.rol,
        password_hash=hash_password(data.password),
        casilla_id=data.casilla_id
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return {
        "mensaje": "Usuario registrado correctamente",
        "usuario_id": usuario.id,
        "clave_de_elector": usuario.clave_de_elector,
        "rol": usuario.rol
    }


# ── Login ─────────────────────────────────────────────────────────────────────

@router.post("/login", response_model=RespuestaLogin)
def login(data: LoginUsuario, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.clave_de_elector == data.clave_de_elector
    ).first()

    if not usuario or not verify_password(data.password, usuario.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Clave de elector o contraseña incorrectos"
        )

    return RespuestaLogin(
        mensaje="Autenticación exitosa",
        usuario_id=usuario.id,
        clave_de_elector=usuario.clave_de_elector,
        rol=usuario.rol,
        casilla_id=usuario.casilla_id,
        autenticado=True
    )