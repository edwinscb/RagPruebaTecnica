FROM python:3.11

# Definir directorio de trabajo
WORKDIR /app

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app  

# Copiar dependencias e instalarlas primero
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el backend
COPY . /app

# Ejecutar los scripts en orden y luego iniciar Flask
ENTRYPOINT ["sh", "-c", "python services/extract_text.py && python services/embeddings.py && python api.py"]
