import random
from faker import Faker
from app import create_app, db  # Asegúrate de que esto sea correcto
from app.models import User  # Asegúrate de que esto sea correcto

fake = Faker()

def create_fake_users(num_users):
    for _ in range(num_users):
        user = User(
            email=fake.email(),
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password_hash=User().set_password('password'),  # Hashear la contraseña
            gender=fake.random_element(elements=('Male', 'Female', 'Other')),
            sexual_preferences=fake.random_element(elements=('Heterosexual', 'Homosexual', 'Bisexual')),
            biography=fake.text(),
            fame_rating=random.uniform(0, 10),  # Genera un número aleatorio entre 0 y 10
            profile_picture=fake.image_url(),
            location=fake.city(),
            latitude=fake.latitude(),
            longitude=fake.longitude(),
            is_active=True
        )
        db.session.add(user)

    db.session.commit()

if __name__ == "__main__":
    app = create_app()  # Crear la aplicación
    with app.app_context():  # Establecer el contexto de la aplicación
        create_fake_users(100)  # Generar 100 usuarios




