import json

def search_credential(api_name):

    with open("./settings/api_key.json") as f:
        data = json.load(f)

    if api_name in data:
        return data[api_name]
