# Imagen base oficial de Python
FROM python:3.12-slim

# Instalar dependencias del sistema necesarias (incluye Docker CLI)
RUN apt-get update && apt-get install -y docker.io curl && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar solo archivos necesarios primero para aprovechar caché
COPY requirements.txt ./

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt || pip install flask docker requests

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto
EXPOSE 8080

# Comando por defecto
CMD ["python", "web_ui.py"]
