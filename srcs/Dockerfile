# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/15 12:48:46 by xmatute-          #+#    #+#              #
#    Updated: 2024/11/23 18:00:00 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
# Usa una imagen base ligera de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt y luego instálalo
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente desde la carpeta srcs al contenedor en /app
COPY ./flask /app

# Copia el archivo .env desde la carpeta srcs al contenedor en /app/.env
COPY .env /app/.env

# Expón el puerto que utilizará la aplicación Flask (por ejemplo, 5000)
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]







