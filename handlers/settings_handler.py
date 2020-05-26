import json
import sys
import os

def get_setting(setting):
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
    driver_path = os.path.join(application_path, 'user_files/settings.json')
    with open(driver_path, "r") as file:
        settings = json.load(file)

    return settings[setting]

def get_all_settings():
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
    driver_path = os.path.join(application_path, 'user_files/settings.json')
    with open(driver_path, "r") as file:
        settings = json.load(file)

    return settings

def set_setting(setting, value):
    # can both ADD and EDIT values in a dict so use this for both
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
    driver_path = os.path.join(application_path, 'user_files/settings.json')
    with open(driver_path, "r") as file:
        settings = json.load(file)

    settings[setting] = value

    with open(driver_path, "w") as file:
        json.dump(settings, file)

def check_valid():
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
    driver_path = os.path.join(application_path, 'user_files/settings.json')
    with open(driver_path, "r") as file:
        settings = json.load(file)

    if settings["valid"]:
        return True
    else:
        return False