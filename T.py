import sys
from io import BytesIO

import requests
from PIL import Image


def ocr(geocoder_request):
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = \
            json_response["response"]["GeoObjectCollection"]["featureMember"][
                0][
                "GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        return toponym_coodrinates


search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address_ll = " ".join(sys.argv[1:])

sp = ocr(
    f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-"
    f"98533de7710b&geocode={address_ll}&format=json").split()

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": f"{str(sp[0])},{str(sp[1])}",
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    pass
json_response = response.json()
count = 0
toch = []
for i in range(10):
    pm = ''
    organization = json_response["features"][count]
    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])
    time = organization["properties"]["CompanyMetaData"]
    if "Hours" in organization["properties"]["CompanyMetaData"]:
        ti = time["Hours"]["text"]
        if "круглосуточно" in ti or "24" in ti:
            pm = "pm2dgl"
        else:
            pm = "pm2rdl"
    else:
        pm = "pm2grl"
    toch.append([org_point, pm])
    count += 1
delta = "0.05"
map_params = {
    "ll": f"{str(sp[0])},{str(sp[1])}",
    "spn": ",".join([delta, delta]),
    "l": "map",
    "pt": "{0},{1}~{2},{3}~{4},{5}~{6},{7}~{8},{9}~{10},{11}~{12},{13}~{14},"
          "{15}~{16},{17}~{18},{19}".format(
        toch[0][0], toch[0][1], toch[1][0], toch[1][1], toch[2][0], toch[2][1],
        toch[3][0], toch[3][1], toch[4][0], toch[4][1], toch[5][0], toch[5][1],
        toch[6][0], toch[6][1], toch[7][0], toch[7][1], toch[8][0], toch[8][1],
        toch[9][0], toch[9][1])
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()
