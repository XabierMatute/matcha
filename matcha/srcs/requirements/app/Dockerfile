# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/15 12:48:46 by xmatute-          #+#    #+#              #
#    Updated: 2024/11/15 18:51:17 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM python:3.10.12-alpine

# Etiqueta del mantenedor
LABEL maintainer="xmatute- <xmatute-@student.42.fr>"

EXPOSE 5000

WORKDIR /app

COPY ./requirements.txt ./tmp/requirements.txt

# instalar flask
RUN pip install --upgrade pip
RUN pip install -r ./tmp/requirements.txt
RUN rm -rf ./tmp

# CMD  ["python3", "run.py"]
ENV FLASK_APP=run.py
ENV FLASK_ENV=development


CMD [ "python3", "-m" , "flask", "--debug", "run", "--host=0.0.0.0"]