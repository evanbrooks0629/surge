import json

def get_all_proxies():
    with open("user_files/proxies.json", "r") as file:
        proxies = json.load(file)

    return proxies

def get_proxy(index):
    with open("user_files/proxies.json", "r") as file:
        proxies = json.load(file)

    return proxies[index]

def get_num_proxies():
    with open("user_files/proxies.json", "r") as file:
        proxies = json.load(file)

    return len(proxies)

def insert_proxies(proxies):
    with open("user_files/proxies.json", "w") as file:
        json.dump(proxies, file)
