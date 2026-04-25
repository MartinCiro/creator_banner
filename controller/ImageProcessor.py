from PIL import Image
from typing import Tuple
from io import BytesIO
from base64 import b64encode

class ImageProcessor:
    """
    Utilidades adicionales para procesamiento de imágenes
    """
    
    @staticmethod
    def resize_image(image_bytes: bytes, max_size: Tuple[int, int]) -> bytes:
        """Redimensiona una imagen manteniendo aspect ratio"""
        img = Image.open(BytesIO(image_bytes))
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    
    @staticmethod
    def to_base64(image_bytes: bytes, mime_type: str = "image/png") -> str:
        """Convierte bytes a base64"""
        b64 = b64encode(image_bytes).decode("utf-8")
        return f"data:{mime_type};base64,{b64}"