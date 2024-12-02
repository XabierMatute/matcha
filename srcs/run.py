# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    run.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 11:23:53 by xmatute-          #+#    #+#              #
#    Updated: 2024/11/20 11:43:38 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from app import create_app
from config import RunConfig as Config

app = create_app()

if __name__ == '__main__':
    print(f"Running on {Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)