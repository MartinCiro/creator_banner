from dotenv import load_dotenv
from os import getenv
from dataclasses import dataclass


@dataclass
class RenderConfig:
    width: int
    height: int
    output_dir: str


@dataclass
class TemplateConfig:
    font_family: str
    primary_color: str
    background_color: str


class Config:
    """
    Configuración simple y enfocada para generación de imágenes HTML → PNG
    (Single Responsibility)
    """

    def __init__(self):
        load_dotenv()

        # 🔹 Render settings (Playwright) - Manejar valores vacíos
        width_str = getenv("RENDER_WIDTH", "1024")
        height_str = getenv("RENDER_HEIGHT", "1536")
        
        # Si la variable existe pero está vacía, usar el valor por defecto
        width_val = width_str if width_str and width_str.strip() else "1024"
        height_val = height_str if height_str and height_str.strip() else "1536"
        
        self.render = RenderConfig(
            width=int(width_val),
            height=int(height_val),
            output_dir=getenv("OUTPUT_DIR", "./output/images")
        )

        # 🔹 Template settings (UI)
        self.template = TemplateConfig(
            font_family=getenv("FONT_FAMILY", "Montserrat"),
            primary_color=getenv("PRIMARY_COLOR", "#ec4899"),
            background_color=getenv("BG_COLOR", "#fdf6f6")
        )

        # 🔹 Gemini settings
        self.gemini_api_key = getenv("GEMINI_API_KEY")
        self.gemini_model = getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

    def __repr__(self):
        return (
            f"<Config render=({self.render.width}x{self.render.height}), "
            f"output='{self.render.output_dir}', "
            f"gemini_model='{self.gemini_model}'>"
        )