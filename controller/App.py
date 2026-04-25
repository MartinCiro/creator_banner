from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from controller.BackgroundRemoverAPI import router as bg_router
from uvicorn import run as uv_run
from re import compile, IGNORECASE, sub
from base64 import b64encode

from logging import basicConfig, getLogger, INFO

# Configurar logging
basicConfig(level=INFO)
logger = getLogger(__name__)

class DescriptionRequest(BaseModel):
    name: str

class RoutineRequest(BaseModel):
    nombre: str
    descripcion: str
    product_image: str


class App:
    """
    Aplicación FastAPI con inyección de dependencias
    """
    
    def __init__(self, config, gemini_client, template_generator, renderer, bg_remover=None):
        """
        Inicializa la aplicación con sus dependencias inyectadas
        
        Args:
            config: Configuración de la aplicación
            gemini_client: Cliente de Gemini para generar descripciones
            template_generator: Generador de templates HTML
            renderer: Renderer para convertir HTML a PNG
            bg_remover: Servicio de remoción de fondo (opcional)
        """
        self.config = config
        self.gemini_client = gemini_client
        self.template_generator = template_generator
        self.renderer = renderer
        self.bg_remover = bg_remover
        
        # Crear la aplicación FastAPI
        self.app = FastAPI(
            title="Background Remover & Image Generator",
            description="API para remover fondos y generar imágenes de productos",
            version="1.0.0"
        )
        
        # Configurar templates y archivos estáticos
        self.templates = Jinja2Templates(directory="templates")
        self.app.mount("/static", StaticFiles(directory="static"), name="static")
        
        # Configurar rutas
        self._setup_routes()
 
    def _setup_routes(self):
        """Configura todas las rutas de la aplicación"""
        
        # Incluir routers
        if self.bg_remover:
            self.app.include_router(bg_router)
        
        # Rutas de templates
        @self.app.get("/editor")
        async def editor(request: Request):
            """Editor de imágenes"""
            return self.templates.TemplateResponse("editor.html", {"request": request})
        
        @self.app.post("/description")
        async def generate_description(request: DescriptionRequest):
            """
            Genera una descripción para un producto usando Gemini
            """
            try:
                if not self.gemini_client:
                    raise HTTPException(status_code=503, detail="Servicio Gemini no inicializado")
                
                patron = compile(r'jab[oó]n', IGNORECASE)
                
                # Verificar si contiene "jabón" en el nombre
                if not patron.search(request.name):
                    return JSONResponse({
                        "success": True,
                        "description": "",
                        "message": "El producto no es un jabón"
                    })
                
                # Generar descripción
                description = self.gemini_client.generar_descripcion(request.name)
                
                return JSONResponse({
                    "success": True,
                    "description": description,
                    "product_name": request.name
                })
                
            except Exception as e:
                logger.error(f"Error generando descripción: {e}")
                return JSONResponse({
                    "success": False,
                    "error": str(e)
                }, status_code=500)
            
        @self.app.post("/jbn")
        async def generate_jbn(request: RoutineRequest):
            """
            Genera una imagen de rutina y la devuelve como base64 (sin guardar en disco)
            """
            try:
                if not self.template_generator or not self.renderer:
                    raise HTTPException(status_code=503, detail="Servicio no inicializado")
                
                # Validar datos
                if not request.nombre or not request.descripcion or not request.product_image:
                    raise HTTPException(status_code=400, detail="Faltan campos requeridos: nombre, descripcion u imagen")
                
                # Crear estructura de datos para el template
                data = {
                    "nombre": request.nombre,
                    "descripcion": request.descripcion,
                    "product_image": request.product_image
                }
                
                # Generar HTML desde el template
                html = self.template_generator.render(data)
                print("132")
                # Renderizar a bytes en lugar de archivo
                image_bytes = await self.renderer.html_to_png_bytes_async(html)
                print("135")
                await self.renderer.html_to_png_async(html, "/app/static/a.png")
                print("137")

                # Convertir a base64
                image_base64 = b64encode(image_bytes).decode("utf-8")
                print("141")
                return JSONResponse({
                    "success": True,
                    "image_base64": f"data:image/png;base64,{image_base64}",
                    "filename": f"{request.nombre.replace(' ', '_')}.png"
                })
                
            except Exception as e:
                logger.error(f"Error generando imagen de rutina: {e}")
                return JSONResponse({
                    "success": False,
                    "error": str(e)
                }, status_code=500)
        
        @self.app.get("/")
        async def root():
            """Ruta raíz"""
            endpoints = {
                "/editor": "Editor de imágenes",
                "/description": "Generar descripción con Gemini",
                "/jbn": "Generar imagen de rutina"
            }
            
            if self.bg_remover:
                endpoints.update({
                    "/bg/remove": "Remover fondo de imagen",
                    "/bg/apply-mask": "Aplicar máscara manual",
                    "/bg/info": "Información del servicio"
                })
            
            return {
                "message": "Background Remover & Image Generator API",
                "endpoints": endpoints
            }
    
    def run(self, host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
        """Ejecuta la aplicación FastAPI"""
        uv_run(
            self.app, 
            host=host,
            port=port,
            reload=reload
        )
    
    def get_app(self):
        """Retorna la instancia de FastAPI para uso externo"""
        return self.app