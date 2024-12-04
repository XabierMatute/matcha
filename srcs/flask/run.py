# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    run.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:23:53 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/04 14:51:59 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from config import RunConfig as Config
from flask import Flask
from models.database import Database

app = Flask(__name__)

from blueprints.users import users_bp
from blueprints.likes import likes_bp
from blueprints.notifications import notifications_bp
from blueprints.interests import interests_bp
from blueprints.chat import chat_bp

app.register_blueprint(users_bp)
app.register_blueprint(likes_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(interests_bp)
app.register_blueprint(chat_bp)

from utils.list_routes import list_routes as list_routex

@app.route("/")
def helloworld():
    return list_routex(app)
    
# if __name__ == "__main__":
#     Database.create_tables()
#     app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
@app.route("/routes", methods=["GET"])
def list_routes():
    """Devuelve una lista de todas las rutas registradas en la aplicación."""
    output = []
    for rule in app.url_map.iter_rules():
        output.append({
            "endpoint": rule.endpoint,
            "methods": list(rule.methods),
            "rule": str(rule)
        })
    return jsonify(output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



    
