# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los requisitos al contenedor
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de tu código al contenedor
COPY . .

# Exponer el puerto en el que la app escuchará
EXPOSE 5000

# Comando para ejecutar tu aplicación
ENTRYPOINT ["gunicorn"]
CMD ["-b", "0.0.0.0:5000", "app:app"]

