# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    run.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:23:53 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/03 16:12:13 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# from app import create_app
from config import RunConfig as Config


# app = create_app()

# if __name__ == '__main__':
#     print(f"Running on {Config.HOST}:{Config.PORT}")
#     app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

# import os
# from psycopg import connect

# postgres_db = os.getenv('POSTGRES_DB')
# postgres_user = os.getenv('POSTGRES_USER')
# postgres_password = os.getenv('POSTGRES_PASSWORD')


# try:
#     conn = connect(dbname=postgres_db, user=postgres_user, password=postgres_password, host=postgres_db)
#     print(f"Conectandome con la base de datos {postgres_db} como {postgres_user} password {postgres_password} host postgres_db")
#     # cur = conn.cursor()
#     # cur.execute("CREATE TABLE test (id serial PRIMARY KEY, cosas varchar);")
#     # conn.commit()
#     # print("Table created")
# except Exception as e:
#     print(f"Error: {e}")

from flask import Flask

from app.models.database import Database

app = Flask(__name__)

@app.route("/")
def helloworld():
    return "Hola Bea!"
    
if __name__ == "__main__":
    Database.create_tables()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)



    
