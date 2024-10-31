import random
from faker import Faker
from app import create_app, db
from app.models import User  # Asegúrate de que la ruta sea correcta

fake = Faker()

def create_fake_users(num_users):
    for _ in range(num_users):
        user = User(
            email=fake.email(),
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password_hash=User().set_password('password'),  # Debe usar el método set_password
            gender=fake.random_element(elements=('Male', 'Female', 'Other')),
            sexual_preferences=fake.random_element(elements=('Heterosexual', 'Homosexual', 'Bisexual')),
            biography=fake.text(),
            fame_rating=random.uniform(0, 10),
            profile_picture=f"https://picsum.photos/200/200?random={random.randint(1, 1000)}",
            location=fake.city(),
            latitude=fake.latitude(),
            longitude=fake.longitude(),
            is_active=True
        )
        db.session.add(user)

    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        create_fake_users(100)  # Crea 100 usuarios falsos







