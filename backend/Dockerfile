FROM python:3.10-slim

WORKDIR /app

# Copia el requirements.txt
COPY requirements.txt .

# Instala pip y las dependencias
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu código y el script al contenedor
COPY . .

# Copia el script de espera al contenedor y lo hace ejecutable
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Exponer el puerto en el que la app escuchará
EXPOSE 5000

# Comando para ejecutar tu aplicación con el script de espera
ENTRYPOINT ["/wait-for-db.sh", "db"]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]



