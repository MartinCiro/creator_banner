from fastapi import APIRouter, UploadFile, File, Request
from base64 import b64encode
from fastapi.responses import JSONResponse
from controller.BackgroundRemover import BackgroundRemover
import logging

logger = logging.getLogger(__name__)

# Crear router para las rutas de background remover
router = APIRouter(prefix="/bg", tags=["background-remover"])

# Instancia global del servicio
bg_remover = None


def init_background_remover(model_name: str = "u2net"):
    """Inicializa el servicio de background remover"""
    global bg_remover
    bg_remover = BackgroundRemover(model_name)
    return bg_remover


@router.post("/remove")
async def remove_background(file: UploadFile = File(...)):
    """
    Remueve el fondo de una imagen subida
    """
    try:
        if not bg_remover:
            return JSONResponse(
                {"success": False, "error": "Servicio no inicializado"},
                status_code=503
            )
        
        # Leer archivo
        img_bytes = await file.read()
        
        # Remover fondo
        result_bytes = bg_remover.remove_background(img_bytes)
        
        # Convertir a base64
        b64 = b64encode(result_bytes).decode("utf-8")
        
        return JSONResponse({
            "success": True, 
            "image": f"data:image/png;base64,{b64}"
        })
        
    except Exception as e:
        logger.error(f"Error en remove_background: {e}")
        return JSONResponse(
            {"success": False, "error": str(e)},
            status_code=500
        )


@router.post("/apply-mask")
async def apply_mask(request: Request):
    """
    Aplica una máscara manual a la imagen
    """
    try:
        if not bg_remover:
            return JSONResponse(
                {"success": False, "error": "Servicio no inicializado"},
                status_code=503
            )
        
        body = await request.json()
        
        if "original" not in body or "mask" not in body:
            raise ValueError("Faltan campos 'original' o 'mask'")
        
        # Aplicar máscara
        result_image = bg_remover.apply_mask(
            body["original"],
            body["mask"]
        )
        
        return JSONResponse({
            "success": True,
            "image": result_image
        })
        
    except Exception as e:
        logger.error(f"Error en apply_mask: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e),
            "type": type(e).__name__
        }, status_code=500)


@router.get("/info")
async def get_info():
    """Obtiene información del servicio"""
    return JSONResponse({
        "service": "Background Remover",
        "status": "active" if bg_remover else "not_initialized",
        "model": "u2net"
    })