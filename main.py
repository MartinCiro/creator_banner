from controller.Config import Config
from controller.Template import Template
from controller.Renderer import Renderer

from controller.utils.file import FileUtils


def main():

    # 🔹 1. Inicializar config
    config = Config()

    # 🔹 2. Leer input JSON
    input_path = "vendor/input.json"
    data = FileUtils.read_json(input_path)

    if not data:
        raise ValueError(f"❌ No se pudo leer el archivo: {input_path}")

    # 🔹 3. Generar HTML
    template = Template(config, data)
    html = template.render()

    # 🔹 4. Asegurar directorio de salida
    FileUtils.ensure_dir(config.render.output_dir)

    # 🔹 5. Definir nombre de salida
    output_path = f"{config.render.output_dir}/routine.png"

    # 🔹 6. Renderizar imagen
    renderer = Renderer(config)
    renderer.html_to_png(html, output_path)

    print(f"✅ Imagen generada: {output_path}")


if __name__ == "__main__":
    main()