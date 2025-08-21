# Imagen base Python moderna y ligera
FROM python:3.12-slim

# Evitar bytecode y hacer logs no bufferizados
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema mínimas (curl opcional para debug/healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY app.py .

# Puerto interno de Flask
EXPOSE 5000

# Comando de arranque (gunicorn recomendado para producción)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
