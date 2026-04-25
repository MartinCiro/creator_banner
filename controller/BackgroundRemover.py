from rembg import remove, new_session
from PIL import Image
from io import BytesIO
from base64 import b64encode, b64decode
from numpy import array as np_array, float32, clip, uint8
import logging

logger = logging.getLogger(__name__)


class BackgroundRemover:
    """
    Controlador para remover fondos de imágenes usando rembg
    """
    
    def __init__(self, model_name: str = "u2net"):
        """
        Inicializa el servicio de remoción de fondo
        
        Args:
            model_name: Modelo de rembg (u2net, u2netp, etc)
        """
        self.session = new_session(model_name)
        logger.info(f"BackgroundRemover inicializado con modelo: {model_name}")
    
    def remove_background(self, image_bytes: bytes) -> bytes:
        """
        Remueve el fondo de una imagen
        
        Args:
            image_bytes: Bytes de la imagen original
            
        Returns:
            bytes: Imagen PNG con fondo transparente
        """
        try:
            result_bytes = remove(image_bytes, session=self.session)
            return result_bytes
        except Exception as e:
            logger.error(f"Error removiendo fondo: {e}")
            raise
    
    def apply_mask(self, original_b64: str, mask_b64: str) -> str:
        """
        Aplica una máscara manual a la imagen
        
        Args:
            original_b64: Imagen procesada por rembg (base64)
            mask_b64: Máscara de canvas (base64)
            
        Returns:
            str: Imagen resultante en base64
        """
        try:
            # Decodificar imágenes
            original_bytes = b64decode(original_b64.split(",")[1])
            mask_bytes = b64decode(mask_b64.split(",")[1])
            
            original = Image.open(BytesIO(original_bytes)).convert("RGBA")
            mask_img = Image.open(BytesIO(mask_bytes)).convert("RGBA")
            
            # Ajustar dimensiones
            if original.size != mask_img.size:
                mask_img = mask_img.resize(original.size, Image.Resampling.LANCZOS)
            
            # Procesar máscara
            mask_arr = np_array(mask_img)
            orig_arr = np_array(original)
            
            # Extraer canal R como máscara
            mask_r = mask_arr[:, :, 0].astype(float32)
            orig_alpha = orig_arr[:, :, 3].astype(float32)
            
            # Combinar alphas
            final_alpha = clip((orig_alpha * mask_r) / 255.0, 0, 255).astype(uint8)
            
            # Aplicar máscara
            result_arr = orig_arr.copy()
            result_arr[:, :, 3] = final_alpha
            result = Image.fromarray(result_arr, mode="RGBA")
            
            # Codificar resultado
            buf = BytesIO()
            result.save(buf, format="PNG")
            buf.seek(0)
            b64 = b64encode(buf.read()).decode("utf-8")
            
            return f"data:image/png;base64,{b64}"
            
        except Exception as e:
            logger.error(f"Error aplicando máscara: {e}")
            raise