import requests


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