# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/15 12:48:46 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/02 14:19:18 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM python:3.10.12-alpine

# Etiqueta del mantenedor
LABEL maintainer="xmatute- <xmatute-@student.42.fr>"

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

EXPOSE 5000

WORKDIR /app

COPY ./requirements.txt ./tmp/requirements.txt

# instalar flask
RUN pip install --upgrade pip
RUN pip install -r ./tmp/requirements.txt
RUN rm -rf ./tmp

ENTRYPOINT [ "python3" ]
CMD [ "run.py"]