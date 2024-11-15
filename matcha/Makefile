# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/04 14:58:54 by xmatute-          #+#    #+#              #
#    Updated: 2024/11/15 18:33:13 by xmatute-         ###   ########.fr        #
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

DCYML := $(SRC_DIR)/docker-compose.yml

VLM_DIR := /home/xmatute-/data

DTB_DIR := $(VLM_DIR)/database

WF_DIR := $(VLM_DIR)/webfiles

WHITE = \033[0;37m
RED = \033[0;31m
CYAN = \033[0;36m
GREEN = \033[0;32m
MAGENTA = \033[0;35m

all : $(DCYML)
	docker compose -f $(DCYML) config
	@echo "making all..."
	docker compose -f $(DCYML) up --build --detach
	@echo "$(MAGENTA)$$ASCIIART$(WHITE)"
	docker ps
	docker volume ls
	docker network ls

down :
	docker compose -f $(DCYML) down

up :
	docker compose -f $(DCYML) up

reload : down all

clean :
	docker compose -f $(DCYML) down --volumes
	@echo "$(RED)clean done...$(WHITE)"

fclean : clean
	docker system prune --volumes --force --all
	docker container prune --force
	docker volume prune --force
	-docker volume rm $(docker volume ls -q) #puede dar error
	rm -rf $(DTB_DIR) $(WF_DIR)
	@echo "$(RED)fclean done...$(WHITE)"

re : fclean all

.PHONY : all clean fclean re down up reload