import json
import sys
import os

def get_all_proxies():
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
        application_path = application_path.split("/")
        application_path.remove(application_path[6])
        application_path.remove(application_path[0])
        appstr = '/'
        for char in application_path:
            appstr += char + '/'
        application_path = appstr
    driver_path = os.path.join(application_path, 'user_files/proxies.json')
    with open(driver_path, "r") as file:
        proxies = json.load(file)

    return proxies

def get_proxy(index):
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
        application_path = application_path.split("/")
        application_path.remove(application_path[6])
        application_path.remove(application_path[0])
        appstr = '/'
        for char in application_path:
            appstr += char + '/'
        application_path = appstr
    driver_path = os.path.join(application_path, 'user_files/proxies.json')
    with open(driver_path, "r") as file:
        proxies = json.load(file)

    return proxies[index]

def get_num_proxies():
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
        application_path = application_path.split("/")
        application_path.remove(application_path[6])
        application_path.remove(application_path[0])
        appstr = '/'
        for char in application_path:
            appstr += char + '/'
        application_path = appstr
    driver_path = os.path.join(application_path, 'user_files/proxies.json')
    with open(driver_path, "r") as file:
        proxies = json.load(file)

    return len(proxies)

def insert_proxies(proxies):
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
        application_path = application_path.split("/")
        application_path.remove(application_path[6])
        application_path.remove(application_path[0])
        appstr = '/'
        for char in application_path:
            appstr += char + '/'
        application_path = appstr
    driver_path = os.path.join(application_path, 'user_files/proxies.json')
    with open(driver_path, "w") as file:
        json.dump(proxies, file)
