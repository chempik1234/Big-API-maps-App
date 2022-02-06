import os
import sys

import pygame
import requests
from get_size import get_size, get_organization_coords

x, y = 0, 0
k = 0
zoom_levels_y = [360 / 2 ** i for i in range(18)]
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
pt, address, postal = None, '', False


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
    if postal and "postal_code" in toponym["metaDataProperty"]["GeocoderMetaData"]["Address"].keys():
        toponym_address += ', ' + toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
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
    draw_text([address], address_y, 3, int(font_size) - 1, pygame.Color("black"))
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
    spn_x = 360 / 2 ** k
    spn_y = 180 / 2 ** k
    x = min(max(-180 + spn_x / 2, x), 180 - spn_x / 2)
    y = min(max(-90 + spn_y / 2, y), 90 - spn_y / 2)
    map_params = {
        "ll": str(x) + ',' + str(y),
        "z": k,
        #"spn": str(spn_x) + ',' + str(spn_y),
        "size": str(SCREEN_SIZE[0]) + ',' + str(SCREEN_SIZE[1]),
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
    pripisat = "Не писать"
    if not postal:
        pripisat = "Написать"
    draw_text(["[ALT] Режим: " + rus_modes[mode],
               "[DEL] Убрать метку", "[F1] " + pripisat,
               "почтовый индекс", "в адресе"], SCREEN_SIZE[1] / 45,
              SCREEN_SIZE[0] * 5 / 8, font_size, pygame.Color("black"))
    draw_text(["[ALT] Режим: " + rus_modes[mode],
               "[DEL] Убрать метку", "[F1] " + pripisat,
               "почтовый индекс", "в адресе"], SCREEN_SIZE[1] / 45 - 1,
              SCREEN_SIZE[0] * 5 / 8, font_size, pygame.Color("white"))
    screen.fill(pygame.Color("black"), button_delete_rect)
    draw_text(["Убрать метку"], button_delete_rect[1], button_delete_rect[0],
              int(SCREEN_SIZE[1] * 0.05), pygame.Color("white"))
    search_update()
    address_update()
    pygame.display.flip()


def search_toponym(param_that_replaces_search=None):
    global x, y, pt, k, address
    #address = ''
    if param_that_replaces_search:
        geo = geocoder_coordinates_address(param_that_replaces_search)
    elif search:
        geo = geocoder_coordinates_address(search)
    elif address:
        geo = geocoder_coordinates_address(address)
    else:
        return None
    if geo:
        pt = list(map(float, geo[0].split()))
        if not param_that_replaces_search:
            x, y = pt
            k = index_closest_element(get_size(search)[1], zoom_levels_y)
        address = geo[1]
        update()


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
                k = min(17, k + 1)
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
            elif i.key == pygame.K_F1:
                postal = not postal
                search_toponym(address)
                update()
        elif i.type == pygame.MOUSEBUTTONDOWN:
            if in_rect(i.pos, button_enter_rect) and i.button == 1:
                search_toponym()
            elif in_rect(i.pos, button_delete_rect) and i.button == 1:
                pt = None
                address = ''
                update()
            elif not in_rect(i.pos, [address_x, address_y, SCREEN_SIZE[0], SCREEN_SIZE[1] - address_y]):
                xx, yy = i.pos
                spn_x = 360 / 2 ** k
                spn_y = 180 / 2 ** k
                yy = SCREEN_SIZE[1] - yy
                xx = (xx / SCREEN_SIZE[0]) * spn_x * 1.175
                xx += x - spn_x * 0.5 * 1.175
                a = yy / SCREEN_SIZE[1]
                yy = (yy / SCREEN_SIZE[1]) * spn_y# * 1.6
                yy += y - spn_y * 0.5# * 1.6
                if i.button == 1:
                    search_toponym(str(xx) + ',' + str(yy))
                elif i.button == 3:
                    coords = get_organization_coords(xx, yy)
                    pt = None
                    if coords:
                        xx, yy = coords
                        search_toponym(str(xx) + ',' + str(yy))
                        pt = coords
                #else:
                #    print(xx, yy)
                #    pt = (xx, yy)
                #    update()
    pass
pygame.quit()
os.remove(map_)