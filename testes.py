import requests
import json

# As chaves para utilização são:
# Client ID: 9b00bac5d16edf381a4d34b27654b5f7
# Client Secret: 4c9a177941edaf96751639cac71255e6
# API User: 1624640222434
# API Secret: cmVuYXRvbW9yZW5AdGVjbm9tZWRpLmNvbS5icjAuNzc4NzEwODI2MDYzOTUzNzE2MjQ2NDAyMjI0MzQ=


def autentication_by_password():
    url = "https://api.plugg.to/oauth/token"
    client_id = "9b00bac5d16edf381a4d34b27654b5f7"
    client_secret = "4c9a177941edaf96751639cac71255e6"
    username = "1624640222434"
    password = "cmVuYXRvbW9yZW5AdGVjbm9tZWRpLmNvbS5icjAuNzc4NzEwODI2MDYzOTUzNzE2MjQ2NDAyMjI0MzQ="
    grant_type = "password"
    payload = "client_id={0}&client_secret={1}&username={2}&password={3}&grant_type={4}".format(
        client_id,
        client_secret,
        username,
        password,
        grant_type
    )

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    jsondict = json.loads(response.text)
    access_token = jsondict["access_token"]

    return access_token


def get_all_orders(access_token):
    import requests

    url = "https://api.plugg.to/orders"

    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type": "application/json"
    }

    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text)


def get_one_product(access_token, sku):
    url = "https://api.plugg.to/skus/{0}".format(sku)

    headers = {
        "Authorization": "Bearer {0}".format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.request("GET", url, headers=headers)

    return json.loads(response.text)


def get_json_len(jsonstr: str, keys: str):
    odict: dict = json.loads(jsonstr)
    lista = keys.split("|")
    for key in lista:
        if not key.isnumeric():
            odict = odict[key]
        else:
            odict = odict[int(key)]

    return len(odict)


def get_json_value(jsonstr: str, keys: str):
    odict: dict = json.loads(jsonstr)
    lista = keys.split("|")
    for key in lista:
        if not key.isnumeric():
            odict = odict[key]
        else:
            odict = odict[int(key)]

    return odict


token: str = autentication_by_password()
json.d
print("OK", "JOAO", "MARI", end="", sep="")


