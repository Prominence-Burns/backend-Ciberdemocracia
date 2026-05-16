from fastapi import FastAPI
from app.routers import (
    polling_stations,
    users,
    ballots,
    tally_sheets,
    events,
    inconsistencies,
    results
)

app = FastAPI(
    title="CIberdemocracia API",
    description="Sistema de auditoría electoral con IA",
    version="1.0.0"
)

app.include_router(polling_stations.router)
app.include_router(users.router)
app.include_router(ballots.router)
app.include_router(tally_sheets.router)
app.include_router(events.router)
app.include_router(inconsistencies.router)
app.include_router(results.router)

@app.get("/")
def root():
    return {"message": "Ciberdemocracia API funcionando :)"}