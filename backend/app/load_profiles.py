import json
import pandas as pd
from app import db
from app.models import User  # Asegúrate de que la ruta sea correcta

# Ruta al archivo JSON
data_file = 'data/profiles.json'

# Cargar datos desde el archivo JSON
with open(data_file) as f:
    profiles = json.load(f)

# Convertir a DataFrame si prefieres trabajar con pandas
df = pd.DataFrame(profiles)

# Ejemplo de cómo iterar sobre los datos y guardarlos en la base de datos
for _, row in df.iterrows():
    user = User(
        email=row['email'],
        username=row['username'],
        first_name=row['first_name'],
        last_name=row['last_name'],
        gender=row['gender'],
        sexual_preferences=row['sexual_preferences'],
        biography=row['biography'],
        profile_picture=row['profile_picture'],
        location=row['location'],
        latitude=row['latitude'],
        longitude=row['longitude'],
        is_active=row['is_active']
    )
    user.set_password('default_password')  # Asigna una contraseña por defecto o personaliza

    db.session.add(user)

# Guardar los cambios en la base de datos
db.session.commit()

print("Perfiles cargados exitosamente.")
