import os
import sys

import pygame
import requests

x, y = 0, 0
zoom_levels, k = [90, 41, 22, 11] + [i / 10 for i in range(40, 1, -2)] + [0.1, 0.09, 0.07, 0.05, 0.02, 0.01, 0.005], 0
#zoom_k_x, zoom_k_y = 360 // zoom_levels, 180 // zoom_levels
spn_x, spn_y = 0, 0
map = "map.png"
mode = 0
SCREEN_SIZE = [600, 450]


def draw_text(text, text_coord_y, text_coord_x, size_font, color):
    font = pygame.font.Font(None, size_font)
    for line in text:
        string_rendered = font.render(line, 1, color)
        _rect = string_rendered.get_rect()
        text_coord_y += 10
        _rect.top = text_coord_y
        _rect.x = text_coord_x
        text_coord_y += _rect.height
        screen.blit(string_rendered, _rect)


def update():
    global x, y, spn_x, spn_y
    modes = ["map", "sat", "sat,skl"]
    rus_modes = ["карта", "спутник", "гибрид"]
    screen.fill(pygame.Color('gray'), [0, 0] + SCREEN_SIZE)
    draw_text(["Загрузка ..."], SCREEN_SIZE[1] / 3,
              SCREEN_SIZE[0] / 3, SCREEN_SIZE[1] // 5, pygame.Color("white"))
    pygame.display.flip()
    map_request = "http://static-maps.yandex.ru/1.x/"
    spn_y = zoom_levels[k]
    spn_x = spn_y * SCREEN_SIZE[0] / SCREEN_SIZE[1]
    x = min(max(-180 + spn_x / 2, x), 180 - spn_x / 2)
    y = min(max(-90 + spn_y / 2, y), 90 - spn_y / 2)
    map_params = {
        "ll": str(x) + ',' + str(y),
        "spn": str(spn_x) + ',' + str(spn_y),
        "l": modes[mode]
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
    draw_text(["[K] Режим: " + rus_modes[mode]], SCREEN_SIZE[1] / 45,
              SCREEN_SIZE[0] * 2 / 3, SCREEN_SIZE[1] // 15, pygame.Color("black"))
    draw_text(["[K] Режим: " + rus_modes[mode]], SCREEN_SIZE[1] / 45 - 1,
              SCREEN_SIZE[0] * 2 / 3, SCREEN_SIZE[1] // 15, pygame.Color("white"))
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
            elif i.key == pygame.K_UP:
                y += spn_y * 2
                update()
            elif i.key == pygame.K_DOWN:
                y -= spn_y * 2
                update()
            elif i.key == pygame.K_LEFT:
                x -= spn_x * 2
                update()
            elif i.key == pygame.K_RIGHT:
                x += spn_x * 2
                update()
            elif i.key == pygame.K_k:
                mode = (mode + 1) % 3
                update()
    pass
pygame.quit()
os.remove(map)