from fastapi import APIRouter, UploadFile, File, HTTPException
import httpx

router = APIRouter(prefix="/vision", tags=["Visión"])

# URL del sistema de visión — cámbiala por la URL real o ngrok de visión
VISION_URL = "http://localhost:9000/procesar-boleta"

@router.post("/procesar-boleta")
async def procesar_boleta(foto: UploadFile = File(...)):
    """
    Recibe una foto desde la app,
    la reenvía al sistema de visión y
    regresa el JSON AECC generado.
    """

    # 1. Lee el contenido de la foto
    contenido = await foto.read()

    # 2. Valida que sea una imagen
    if not foto.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser una imagen"
        )

    # 3. Reenvía la foto al sistema de visión
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            respuesta = await client.post(
                VISION_URL,
                files={"foto": (foto.filename, contenido, foto.content_type)}
            )
            respuesta.raise_for_status()

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="El sistema de visión no respondió a tiempo"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"No se pudo conectar con el sistema de visión: {str(e)}"
        )

    # 4. Regresa el JSON AECC que generó visión
    return respuesta.json()