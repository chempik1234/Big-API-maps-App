import requests, math


def get_size(address):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {"apikey": api_key, "lang": "ru_RU", "text": address}
    response = requests.get(search_api_server, params=search_params)
    json_response = response.json()
    organization = json_response["features"][0]["properties"]
    toponym_lc, toponym_uc = organization["boundedBy"]
    toponym_size = (abs(toponym_lc[0] - toponym_uc[0]),
                    abs(toponym_lc[1] - toponym_uc[1]))
    return toponym_size


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)

    return distance


def get_organization_coords(x, y):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {"apikey": api_key, "lang": "ru_RU", "text": str(y) + ',' + str(x)}
    response = requests.get(search_api_server, params=search_params)
    json_response = response.json()
    if not json_response["features"]:
        return None
    point, curpoint, long = None, None, None
    for i in range(len(json_response["features"])):
        organization = json_response["features"][i]
        curpoint = organization["geometry"]["coordinates"]
        lonlat = lonlat_distance((x, y), curpoint)
        if not long and lonlat < 50:
            long = lonlat
            point = organization["geometry"]["coordinates"]
        elif long and lonlat < long and lonlat < 50:
            long = lonlat
            point = organization["geometry"]["coordinates"]
    return point