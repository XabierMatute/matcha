# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/04 14:58:54 by xmatute-          #+#    #+#              #
#    Updated: 2024/12/20 10:42:29 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

define ASCIIART

─────▄█▀█▄──▄███▄────❤
────▐█░██████████▌────
─────██▒█████████─────
──────▀████████▀──────
─────────▀██▀─────────

endef
export ASCIIART

NAME := Matcha

DOCKER_APP := '/Applications/Docker.app'

SRC_DIR :=	./srcs

DATABASE_DIR := $(SRC_DIR)/database

DCYML := $(SRC_DIR)/docker-compose.yml

VLM_DIR := /home/xmatute-/data

DTB_DIR := $(VLM_DIR)/database

WF_DIR := $(VLM_DIR)/webfiles

WHITE = \033[0;37m
RED = \033[0;31m
CYAN = \033[0;36m
GREEN = \033[0;32m
MAGENTA = \033[0;35m

all : $(DCYML) $(DATABASE_DIR)
	docker compose -f $(DCYML) config
	@echo "making all..."
	docker compose -f $(DCYML) up --build --detach
	@echo "$(MAGENTA)$$ASCIIART$(WHITE)"
	docker ps
	docker volume ls
	docker network ls
	@echo "web: http://localhost:5000"
	@echo "adminer: http://localhost:8080"

$(DATABASE_DIR) :
	mkdir -p $(DATABASE_DIR)

down :
	docker compose -f $(DCYML) down

up :
	docker compose -f $(DCYML) up

reload : down all

flask_restart :
	docker compose -f $(DCYML) restart flask

flask_logs :
	docker compose -f $(DCYML) logs flask

flask_freeze :
	docker compose -f $(DCYML) exec flask pip freeze

clean :
	docker compose -f $(DCYML) down --volumes
	@echo "$(RED)clean done...$(WHITE)"

fclean : clean
	-bash $(SRC_DIR)/requirements/tools/clean_docker.sh
	@echo "$(RED)fclean done...$(WHITE)"

re : clean all

hard_re : fclean all

.PHONY : all clean fclean re down up reload flask_restart flask_logs flask_freeze hard_re