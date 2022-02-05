import os
import sys

import pygame
import requests

map_request = "http://static-maps.yandex.ru/1.x/"
x, y = 51.0, 54.0
spn_x, spn_y = 180, 90
map_params = {
    "ll": str(x) + ',' + str(y),
    "spn": str(spn_x) + ',' + str(spn_y),
    "l": "map"
}
response = requests.get(map_request, params=map_params)
if not response:
    print("Ошибка выполнения запроса:")
    print(response.url)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)
map = "map.png"
with open(map, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((650, 400))
screen.blit(pygame.image.load(map), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
os.remove(map)