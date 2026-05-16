from fastapi import FastAPI
from app.routers import (
    casillas,
    usuarios,
    boletas,
    actas,
    eventos,
    inconsistencias,
    resultados,
    vision,
    aecc,
    auth                              
)

app = FastAPI(
    title="CIberdemocracia API",
    description="Sistema de auditoría electoral con IA — AECC v1",
    version="2.0.0"
)

app.include_router(casillas.router)
app.include_router(usuarios.router)
app.include_router(boletas.router)
app.include_router(actas.router)
app.include_router(eventos.router)
app.include_router(inconsistencias.router)
app.include_router(resultados.router)
app.include_router(vision.router)
app.include_router(aecc.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"mensaje": "CIberdemocracia API funcionando :)"}