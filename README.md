# 🧼 JabonCreator — Generador de Fichas de Producto con IA

Aplicación web (FastAPI) que genera fichas visuales de productos (jabones) combinando **IA generativa (Gemini)**, **remoción de fondo con deep learning (rembg / U²-Net)** y **renderizado HTML → PNG (Playwright)**. Incluye un editor visual de máscaras en el navegador para ajustar manualmente la segmentación del producto.

---

## 📋 Requisitos y configuración inicial

### 1. Instalar dependencias

#### Windows

```bash
python -m venv venv; venv\Scripts\activate; pip install -r requirements.txt
```

#### Linux

```bash
python -m venv venv; source venv/bin/activate; pip install -r requirements.txt
```

### 2. Instalar navegadores de Playwright

```bash
playwright install chromium
```

### 3. Descargar el modelo de rembg (U²-Net)

```bash
python -c "from rembg import new_session; new_session('u2net')"
```

### 4. Configuración de variables de entorno

Crea un archivo `.env` basado en `example` con esta estructura:

```bash
# 🔑 Gemini API (obligatorio para generación de descripciones)
GEMINI_API_KEY=tu_api_key_de_google_ai_studio
GEMINI_MODEL=gemini-2.0-flash-exp

# 🖼️ Render (Playwright)
RENDER_WIDTH=920
RENDER_HEIGHT=380

# 🎨 Template (UI)
FONT_FAMILY=Montserrat
PRIMARY_COLOR=#6b2348
BG_COLOR=#fdf6f6

# 📁 Rutas
OUTPUT_DIR=./output/images
```

> **Nota**: Puedes obtener una API key gratuita de Gemini en [Google AI Studio](https://aistudio.google.com/).

### 5. Ejecución

#### Local (Python)

```bash
python main.py
```

#### Docker Compose

```bash
docker compose up --build
```

La aplicación quedará disponible en `http://localhost:8000`.

---

## 🐳 Docker

El proyecto incluye un `Dockerfile` basado en `python:3.11-slim` con:

- Librerías del sistema para **Playwright/Chromium** (`libnss3`, `libatk-bridge2.0-0`, etc.)
- Librerías para **rembg/Pillow** (`libgl1`, `libglib2.0-0`, etc.)
- **Fuentes** (`fonts-dejavu-core`, `fonts-liberation`, `fonts-noto-core`) para evitar problemas de renderizado
- Descarga del modelo **u2net** durante el build
- Chromium de Playwright preinstalado

```bash
docker compose up --build
```

El `docker-compose.yml` monta volúmenes para **hot-reload** en desarrollo y persiste la caché del modelo y de Playwright.

---

## 📂 Estructura del Proyecto

```
.
├── controller/
│   ├── App.py                    # FastAPI + rutas
│   ├── Config.py                 # Configuración (.env)
│   ├── GeminiClient.py           # 🤖 Cliente de IA generativa (Gemini 2.5 Flash)
│   ├── BackgroundRemover.py      # 🧠 Remoción de fondo con U²-Net
│   ├── BackgroundRemoverAPI.py   # Endpoints /bg/*
│   ├── ImageProcessor.py         # Utilidades de imagen
│   ├── Log.py                    # Sistema de logs
│   ├── Renderer.py               # HTML → PNG (Playwright async)
│   ├── Template.py               # Generador de HTML (ficha de producto)
│   └── utils/
│       ├── crypto.py
│       ├── file.py
│       ├── http.py
│       ├── random_utils.py
│       └── time_utils.py
├── static/
│   ├── a.js                      # MaskEditor (canvas + máscara)
│   ├── st.css                    # Estilos del editor
│   └── icon.png
├── templates/
│   └── editor.html               # UI del editor
├── vendor/
│   ├── input.json                # Datos de producto (ejemplo)
│   ├── icon.svg
│   └── favicon.ico
├── main.py                       # Entry point (FastAPI)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🏗️ Arquitectura del Sistema

```mermaid
graph TB
    subgraph Cliente["🌐 Cliente (Navegador)"]
        UI[editor.html]
        JS[a.js - MaskEditor]
        UI --- JS
    end

    subgraph API["⚡ FastAPI (App.py)"]
        R1["POST /description"]
        R2["POST /jbn"]
        R3["POST /bg/remove"]
        R4["POST /bg/apply-mask"]
        R5["GET /editor"]
    end

    subgraph IA["🤖 IA / Deep Learning"]
        GEM[GeminiClient<br/>Gemini 2.5 Flash]
        REMBG[BackgroundRemover<br/>U²-Net]
    end

    subgraph Render["🖼️ Renderizado"]
        TPL[Template.py<br/>HTML Generator]
        RND[Renderer.py<br/>Playwright Chromium]
    end

    subgraph Storage["💾 Persistencia"]
        ENV[.env / Config]
        LOGS[logs/]
        OUT[output/images/]
    end

    JS -- "1. Nombre del producto" --> R1
    R1 --> GEM
    GEM -- "Descripción" --> JS

    JS -- "2. Imagen subida" --> R3
    R3 --> REMBG
    REMBG -- "PNG sin fondo" --> JS

    JS -- "3. Ajuste máscara" --> R4
    R4 --> REMBG

    JS -- "4. Datos + imagen" --> R2
    R2 --> TPL
    TPL -- "HTML" --> RND
    RND -- "PNG" --> R2
    R2 -- "Base64" --> JS

    ENV -.-> API
    ENV -.-> IA
    API -.-> LOGS
    RND -.-> OUT

    style IA fill:#ffe4e6,stroke:#be123c,stroke-width:2px
    style Render fill:#dbeafe,stroke:#1d4ed8,stroke-width:2px
    style Cliente fill:#dcfce7,stroke:#16a34a,stroke-width:2px
    style API fill:#fef3c7,stroke:#ca8a04,stroke-width:2px
```

---

## 🔄 Flujo de Funcionamiento

### Flujo completo (de la imagen al PNG final)

```mermaid
sequenceDiagram
    autonumber
    actor U as 👤 Usuario
    participant W as 🌐 editor.html
    participant A as ⚡ FastAPI
    participant G as 🤖 Gemini
    participant R as 🧠 rembg (U²-Net)
    participant T as 📄 Template
    participant P as 🖼️ Playwright

    U->>W: Sube imagen (drag & drop)
    W->>A: POST /bg/remove (imagen)
    A->>R: remove(image_bytes)
    R-->>A: PNG sin fondo
    A-->>W: data:image/png#59;base64,...

    Note over W: Carga en MaskEditor<br/>(original, mask, main)

    U->>W: Ajusta máscara (pincel)
    W->>A: POST /bg/apply-mask (original + mask)
    A->>R: apply_mask(original, mask)
    R-->>A: PNG compuesto
    A-->>W: data:image/png#59;base64,...

    alt Nombre contiene "jabón"
        W->>A: POST /description (nombre)
        A->>G: generar_descripcion(nombre)
        G-->>A: Texto 180-220 chars
        A-->>W: {description}
        Note over W: Carga descripción en notas
    end

    U->>W: Click "Exportar"
    W->>A: POST /jbn (nombre, descripción, imagen)
    A->>T: render(data)
    T-->>A: HTML
    A->>P: html_to_png_bytes_async(HTML)
    P-->>A: PNG bytes
    A-->>W: {image_base64, filename}
    W->>U: Descarga PNG
```

### Flujo del cliente de IA (Gemini)

```mermaid
graph TD
    A[Nombre del producto] --> B{¿Contiene 'jabón'?}
    B -->|No| Z[Retorna vacío]
    B -->|Sí| C[GeminiClient.generar_descripcion]
    C --> D[Construir prompt base]
    D --> E[Llamada a Gemini 2.5 Flash]
    E --> F{Longitud válida?}
    F -->|< 150| G[Expandir prompt]
    F -->|> 250| H[Acortar a primera oración]
    F -->|180-220| I[Limpieza de respuesta]
    G --> I
    H --> I
    I --> J[Eliminar prefijos/comillas]
    J --> K[Descripción final]
    K --> L[Cargar en notes-textarea]

    style C fill:#ffe4e6,stroke:#be123c,stroke-width:2px
```

### Flujo del editor de máscaras (frontend)

```mermaid
graph TD
    A[Imagen cargada] --> B[Canvas original]
    A --> C[Canvas mask - blanco]
    A --> D[Canvas main - compuesto]
    B --> E[MaskEditor render]
    C --> E
    E --> D
    F[Usuario pinta] --> G{Tool?}
    G -->|erase| H[Alpha *= mask_value]
    G -->|add| I[Alpha = 255 en zona pintada]
    H --> D
    I --> D
    D --> J[getCompositeDataUrl]
    J --> K[POST /jbn]
```

---

## 🔌 Endpoints de la API

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Info general y listado de endpoints |
| `GET` | `/editor` | UI del editor de máscaras |
| `POST` | `/description` | Genera descripción con **Gemini** |
| `POST` | `/jbn` | Genera imagen final (HTML → PNG) |
| `POST` | `/bg/remove` | Remueve fondo con **U²-Net** |
| `POST` | `/bg/apply-mask` | Aplica máscara manual |
| `GET` | `/bg/info` | Estado del servicio de rembg |

---

## 🤖 Componentes de IA

| Componente | Tecnología | Uso |
|---|---|---|
| **GeminiClient** | Gemini 2.5 Flash (Google) | Generación de descripciones de producto |
| **BackgroundRemover** | rembg + **U²-Net** | Segmentación y remoción de fondo |
| **MaskEditor** | Canvas API (JS) | Ajuste manual de la máscara de segmentación |

---

## 🛠 Herramientas de desarrollo

### Actualizar dependencias

```bash
pip install pipreqs; pipreqs . --force
```

### Comprimir/Descomprimir paquetes offline

#### Windows

```bash
Compress-Archive -Path .\offline_packages\* -DestinationPath offline_packages.zip -CompressionLevel Optimal
Expand-Archive -Path offline_packages.zip -DestinationPath packages
```

#### Linux

```bash
zip -9 -r offline_packages.zip ./offline_packages/
unzip offline_packages.zip -o packages
```

### Modo Offline

```bash
# Instalar desde paquetes locales
pip install --no-index --find-links packages -r requirements.txt

# Descargar paquetes
pip download -r requirements.txt -d ./offline_packages --only-binary :all:
```

### Compilar a ejecutable (.exe)

```bash
python -m PyInstaller --icon="vendor/favicon.ico" --onefile --windowed main.py
```

---

## 🎨 Personalización

Edita el archivo `.env` para cambiar:

- **Fuente**: `FONT_FAMILY=Montserrat`
- **Color primario**: `PRIMARY_COLOR=#6b2348`
- **Fondo**: `BG_COLOR=#fdf6f6`
- **Tamaño de render**: `RENDER_WIDTH=920`, `RENDER_HEIGHT=380`

El template (`controller/Template.py`) genera la ficha con:

- Imagen del producto con `clip-path` diagonal
- Ramas decorativas SVG con color dinámico
- Título, descripción y footer "100% NATURALES Y ECOLÓGICOS"

---

#### 💡 **Créditos**

[Plantilla base](https://github.com/villalbaluis/arquitectura-bots-python) proporcionada por [Luis Villalba](https://github.com/villalbaluis)
