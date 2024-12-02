# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    list_routes.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 12:45:49 by xmatute-          #+#    #+#              #
#    Updated: 2024/11/20 19:52:00 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def list_routes(app, url_prefix: str = ""):
    # Obtener todas las reglas de URL
    rules = [rule for rule in app.url_map.iter_rules() if rule.rule.startswith(url_prefix)]
    # Generar enlaces HTML para cada ruta
    links = [f'<a href="{rule.rule}">{rule.rule}</a>' for rule in rules]
    # Renderizar la lista de enlaces como HTML
    return "<br>".join(links)
