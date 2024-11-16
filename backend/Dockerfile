# Usar una imagen base más ligera y optimizada para producción
FROM python:3.10-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar primero los archivos de requerimientos para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar las dependencias sin usar caché para mantener la imagen pequeña
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el archivo .env si es necesario para la configuración del entorno
# Recomiendo pasar las variables de entorno en lugar de copiar directamente el archivo .env
# COPY .env ./

# Crear un usuario no root para ejecutar la aplicación
RUN adduser --disabled-password --gecos '' appuser

# Cambiar al usuario creado para mayor seguridad
USER appuser

# Copiar el resto del código de la aplicación al contenedor
COPY . .

# Exponer el puerto en el que la app estará corriendo
EXPOSE 5000

# Comando para ejecutar la aplicación con Gunicorn
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000"]

# El CMD es el archivo de entrada que Gunicorn debe cargar
# Cambia app:app si tu aplicación Flask está en otro archivo o módulo
CMD ["app.app:app"]








