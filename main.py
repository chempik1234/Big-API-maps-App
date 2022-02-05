import os
import sys

import pygame
import requests

x, y = 51.0, 54.0
zoom_levels, k = [90, 41, 22, 11] + [i / 10 for i in range(40, 1, -1)], 0
print(zoom_levels)
#zoom_k_x, zoom_k_y = 360 // zoom_levels, 180 // zoom_levels
spn_x, spn_y = 180.0, 90.0
map = "map.png"
SCREEN_SIZE = [600, 450]


def update():
    map_request = "http://static-maps.yandex.ru/1.x/"
    spn_y = zoom_levels[k]
    spn_x = spn_y * 4 / 3
    map_params = {
        "ll": str(x) + ',' + str(y),
        "spn": str(spn_x) + ',' + str(spn_y),
        "l": "map"
    }
    response = requests.get(map_request, params=map_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")", response.content)
        sys.exit(1)
    with open(map, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map), (0, 0))
    pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
update()
running = True
while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_PAGEUP:
                k = max(0, k - 1)
                update()
            elif i.key == pygame.K_PAGEDOWN:
                k = min(len(zoom_levels) - 1, k + 1)
                update()
    pass
pygame.quit()
os.remove(map)