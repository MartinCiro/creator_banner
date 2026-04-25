FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para rembg, Playwright y Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Para rembg y Pillow
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    # Para Playwright (Chromium)
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    # Utilitarios
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt primero (mejor caché)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Playwright y los navegadores (Chromium)
RUN playwright install chromium

# Descargar el modelo u2net durante el build (para rembg)
RUN python -c "from rembg import new_session; new_session('u2net')"

# Copiar el resto de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p logs static templates

# ✅ EXPONER el puerto
EXPOSE 8000

# ✅ AÑADIR el CMD (asumiendo que usas FastAPI/uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]