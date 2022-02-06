import os
import sys

import pygame
import requests
from get_size import get_size

x, y = 0, 0
zoom_levels, k = [90, 41, 22, 11] + [i / 10 for i in range(40, 1, -2)] + [0.1, 0.09, 0.07, 0.05, 0.02, 0.01, 0.005], 0
#zoom_k_x, zoom_k_y = 360 // zoom_levels, 180 // zoom_levels
spn_x, spn_y = 0, 0
map_, mode, search = "map.png", 0, ""
SCREEN_SIZE = [600, 450]
sqr_sizex, sqr_sizey, sqr_y = SCREEN_SIZE[0] * .9, SCREEN_SIZE[1] * .1,  SCREEN_SIZE[1] * .9
address_x, address_y, address_size_x, address_size_y = 0, SCREEN_SIZE[1] * 0.825, SCREEN_SIZE[0] * 0.75, SCREEN_SIZE[1] * 0.075
button_enter_rect = [sqr_sizex, sqr_y, SCREEN_SIZE[0] * .1, sqr_sizey]
button_delete_rect = [address_size_x, SCREEN_SIZE[1] * 0.85, SCREEN_SIZE[0] * 0.25, SCREEN_SIZE[1] * 0.05]
text_keys = {pygame.K_1: '1',
             pygame.K_2: '2',
             pygame.K_3: '3',
             pygame.K_4: '4',
             pygame.K_5: '5',
             pygame.K_6: '6',
             pygame.K_7: '7',
             pygame.K_8: '8',
             pygame.K_9: '9',
             pygame.K_0: '0',
             pygame.K_MINUS: '-',
             pygame.K_q: 'й',
             pygame.K_w: 'ц',
             pygame.K_e: 'у',
             pygame.K_r: 'к',
             pygame.K_t: 'е',
             pygame.K_y: 'н',
             pygame.K_u: 'г',
             pygame.K_i: 'ш',
             pygame.K_o: 'щ',
             pygame.K_p: 'з',
             pygame.K_LEFTBRACKET: 'х',
             pygame.K_RIGHTBRACKET: 'ъ',
             pygame.K_a: 'ф',
             pygame.K_s: 'ы',
             pygame.K_d: 'в',
             pygame.K_f: 'а',
             pygame.K_g: 'п',
             pygame.K_h: 'р',
             pygame.K_j: 'о',
             pygame.K_k: 'л',
             pygame.K_l: 'д',
             pygame.K_SEMICOLON: 'ж',
             pygame.K_QUOTE: 'э',
             pygame.K_z: 'я',
             pygame.K_x: 'ч',
             pygame.K_c: 'с',
             pygame.K_v: 'м',
             pygame.K_b: 'и',
             pygame.K_n: 'т',
             pygame.K_m: 'ь',
             pygame.K_COMMA: 'б',
             pygame.K_PERIOD: 'ю',
             pygame.K_SLASH: '.',
             pygame.K_SPACE: ' '}
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "format": "json",
}
pt, address = None, ''


def index_closest_element(elem, list_):
    dif, cur_dif, k = None, None, 0
    for i in range(len(list_)):
        cur_dif = abs(list_[i] - elem)
        if not dif:
            dif = cur_dif
            k = i
        elif dif > cur_dif:
            dif = cur_dif
            k = i
    return k


def geocoder_coordinates_address(geocode):
    geocoder_params["geocode"] = geocode
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        sys.exit()
    json_response = response.json()
    results = json_response["response"]["GeoObjectCollection"]["featureMember"]
    if not results:
        return None
    toponym = results[0]["GeoObject"]
    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]
    toponym_coodrinates = toponym["Point"]["pos"]
    return toponym_coodrinates, toponym_address


def in_rect(xy, xywh):
    x, y = xy
    x1, y1, w, h = xywh
    return x1 <= x <= x1 + w and y1 <= y <= y1 + h


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


def get_rect_str(text, text_coord_y, text_coord_x, size_font):
    font = pygame.font.Font(None, size_font)
    rects = []
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        _rect = string_rendered.get_rect()
        text_coord_y += 10
        _rect.top = text_coord_y
        _rect.x = text_coord_x
        text_coord_y += _rect.height
        rects.append(_rect)
    return rects


def search_update():
    font_size = int(sqr_sizey) - 4
    if search:
        font_size *= min(1, sqr_sizex / get_rect_str([search], sqr_y + 3, 3, font_size)[0].width)
    screen.fill(pygame.Color("black"), [0, sqr_y, sqr_sizex, sqr_sizey])
    screen.fill(pygame.Color("white"), [1, sqr_y + 1, sqr_sizex - 2, sqr_sizey - 2])
    screen.fill(pygame.Color("red"), button_enter_rect)
    draw_text([search], sqr_y + 3, 3, int(font_size) - 1, pygame.Color("black"))
    pygame.display.flip()


def address_update():
    font_size = int(sqr_sizey) - 4
    if address:
        font_size *= min(1, address_size_x / get_rect_str([address], address_y + 3, 3, font_size)[0].width)
    screen.fill(pygame.Color("black"), [0, address_y, address_size_x, address_size_y])
    screen.fill(pygame.Color("gray"), [1, address_y + 1, address_size_x - 2, address_size_y - 2])
    draw_text([address], address_y + 3, 3, int(font_size) - 1, pygame.Color("black"))
    pygame.display.flip()


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
    if pt:
        map_params["pt"] = str(pt[0]) + ',' + str(pt[1]) + ',pma'
    response = requests.get(map_request, params=map_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")", response.content)
        sys.exit(1)
    with open(map_, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_), (0, 0))
    font_size = SCREEN_SIZE[1] // 15
    draw_text(["[ALT] Режим: " + rus_modes[mode]], SCREEN_SIZE[1] / 45,
              SCREEN_SIZE[0] * 5 / 8, font_size, pygame.Color("black"))
    draw_text(["[ALT] Режим: " + rus_modes[mode]], SCREEN_SIZE[1] / 45 - 1,
              SCREEN_SIZE[0] * 5 / 8, font_size, pygame.Color("white"))
    draw_text(["[DEL] Убрать метку"], SCREEN_SIZE[1] / 45 + font_size,
              SCREEN_SIZE[0] * 5 / 8, font_size, pygame.Color("black"))
    draw_text(["[DEL] Убрать метку"], SCREEN_SIZE[1] / 45 - 1 + font_size,
              SCREEN_SIZE[0] * 5 / 8, font_size, pygame.Color("white"))
    screen.fill(pygame.Color("black"), button_delete_rect)
    draw_text(["Убрать метку"], button_delete_rect[1], button_delete_rect[0],
              int(SCREEN_SIZE[1] * 0.05), pygame.Color("white"))
    search_update()
    address_update()
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
            elif i.key == pygame.K_LALT or i.key == pygame.K_RALT:
                mode = (mode + 1) % 3
                update()
            elif i.key in text_keys.keys():
                search += text_keys[i.key]
                search_update()
            elif i.key == pygame.K_BACKSPACE and search:
                search = search[: -1]
                search_update()
            elif i.key == pygame.K_DELETE:
                pt = None
                address = None
                update()
        elif i.type == pygame.MOUSEBUTTONDOWN:
            if in_rect(i.pos, button_enter_rect) and i.button == 1:
                geo = geocoder_coordinates_address(search)
                if geo:
                    x, y = list(map(float, geo[0].split()))
                    pt = (x, y)
                    address = geo[1]
                    k = index_closest_element(get_size(search)[1], zoom_levels)
                    update()
            elif in_rect(i.pos, button_delete_rect) and i.button == 1:
                pt = None
                address = ''
                update()
    pass
pygame.quit()
os.remove(map_)