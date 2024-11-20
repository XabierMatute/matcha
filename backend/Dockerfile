# Usar una imagen base con Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de la aplicación al contenedor
COPY . /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usarás para la app
EXPOSE 5000

# Definir el comando para ejecutar el servidor con Gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]









