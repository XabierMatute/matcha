# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    list_routes.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/20 12:45:49 by xmatute-          #+#    #+#              #
#    Updated: 2024/11/20 12:48:31 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def list_routes(app):
    # Obtener todas las reglas de URL
    rules = app.url_map.iter_rules()
    # Generar enlaces HTML para cada ruta
    links = [f'<a href="{rule.rule}">{rule.rule}</a>' for rule in rules]
    # Renderizar la lista de enlaces como HTML
    return "<br>".join(links)