# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:50:53 by xmatute-          #+#    #+#              #
#    Updated: 2024/11/20 13:04:04 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Blueprint
# from .view import view

bp = Blueprint('fake_users', __name__, url_prefix="/fake_users")

# @bp.route("/fake_users")
# def root():
#     return view()
    
import os
from flask import Blueprint, render_template_string, request, current_app
from psycopg import connect
import faker

fake = faker.Faker()

# Define el Blueprint
# fake_users_bp = Blueprint('fake_users', __name__)

# Variables de conexión a la base de datos (ajusta según tu configuración)
postgres_db = os.getenv('POSTGRES_DB')
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')

@bp.route("/")
def fake_users():
    # Obtener todas las reglas de URL
    rules = current_app.url_map.iter_rules()
    # Generar enlaces HTML para cada ruta
    links = [f'<a href="{rule.rule}">{rule.rule}</a>' for rule in rules if "fake_users" in rule.rule]
    # Renderizar la lista de enlaces como HTML
    return render_template_string("<br>".join(links))

@bp.route("/create_table")
def create_table():
    try:
        conn = connect(dbname=postgres_db, user=postgres_user, password=postgres_password, host='postgres_db')
        cur = conn.cursor()
        cur.execute("CREATE TABLE fake_users (id serial PRIMARY KEY, name varchar);")
        conn.commit()
        return "<p>Table created</p>"
    except Exception as e:
        return f"<p>Error: {e}</p>"

@bp.route("/insert_fake_user")
def insert_fake_user():
    try:
        conn = connect(dbname=postgres_db, user=postgres_user, password=postgres_password, host='postgres_db')
        cur = conn.cursor()
        cur.execute(f"INSERT INTO fake_users (name) VALUES ('{fake.first_name()}');")
        conn.commit()
        return "<p>User inserted</p>"
    except Exception as e:
        return f"<p>Error: {e}</p>"

@bp.route("/create_fake_user", methods=["GET", "POST"])
def create_fake_user():
    if request.method == "POST":
        # Obtener el nombre del formulario
        try:
            user_name = request.form["name"]
            conn = connect(dbname=postgres_db, user=postgres_user, password=postgres_password, host='postgres_db')
            cur = conn.cursor()
            cur.execute(f"INSERT INTO fake_users (name) VALUES (%s);", (user_name,))
            conn.commit()
            return f"<p>Fake user {user_name} inserted.</p>"
        except Exception as e:
            return f"<p>Error: {e}</p>"

    # Si es GET, muestra el formulario para crear el usuario
    return render_template_string("""
        <form method="post">
            <label for="name">Enter Fake User's Name:</label>
            <input type="text" name="name" id="name" required>
            <button type="submit">Insert Fake User</button>
        </form>
    """)

@bp.route("/fake_users")
def show_users():
    try:
        conn = connect(dbname=postgres_db, user=postgres_user, password=postgres_password, host='postgres_db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM fake_users;")
        rows = cur.fetchall()
        
        # Generar tabla HTML
        table_html = "<table border='1'><tr><th>ID</th><th>Name</th></tr>"
        for row in rows:
            table_html += f"<tr><td>{row[0]}</td><td>{row[1]}</td></tr>"
        table_html += "</table>"
        
        return table_html
    except Exception as e:
        return f"<p>Error: {e}</p>"