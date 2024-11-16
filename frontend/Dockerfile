# Usar la imagen base oficial de Node.js
FROM node:18-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias
COPY package.json package-lock.json ./

# Instalar las dependencias del frontend
RUN npm install --production

# Copiar el resto del código fuente del frontend
COPY . .

# Construir la aplicación de React para producción
RUN npm run build

# Instalar un servidor HTTP para servir los archivos estáticos (puedes usar nginx o serve)
# Aquí se usa `serve`, pero también puedes usar nginx si lo prefieres

# Instalar `serve` globalmente
RUN npm install -g serve

# Exponer el puerto 3000 (puedes cambiarlo según tu configuración)
EXPOSE 3000

# Ejecutar el servidor estático
CMD ["serve", "-s", "build", "-l", "3000"]
