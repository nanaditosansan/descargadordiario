FROM python:3.13-slim

WORKDIR /app

# Instalamos la única librería externa que usas
RUN pip install requests

# Copiamos tu script al contenedor
COPY download.py .

# Creamos la carpeta donde el contenedor "creerá" que guarda los datos
RUN mkdir /data

# Comando para ejecutar
CMD ["python", "download.py"]

