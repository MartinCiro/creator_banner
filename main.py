from controller.Config import Config
from controller.GeminiClient import GeminiClient
from controller.Template import Template
from controller.Renderer import Renderer
from controller.App import App
from controller.BackgroundRemoverAPI import init_background_remover

# ✅ Crear instancias a nivel global (no dentro de main)
config = Config()
gemini_client = GeminiClient(config)
template_generator = Template(config)
renderer = Renderer(config)

# Background remover (opcional)
bg_remover = None
try:
    bg_remover = init_background_remover()
    print("✅ Background Remover inicializado")
except Exception as e:
    print(f"⚠️ Background Remover no disponible: {e}")

# ✅ Crear la app globalmente
app_instance = App(
    config=config,
    gemini_client=gemini_client,
    template_generator=template_generator,
    renderer=renderer,
    bg_remover=bg_remover
)

# ✅ Exponer la instancia de FastAPI para uvicorn
app = app_instance.get_app()

# Mantener la función main para ejecución directa
def main():
    """Ejecuta el servidor (para python main.py)"""
    app_instance.run()

if __name__ == "__main__":
    main()