import json

def get_setting(setting):
    with open("user_files/settings.json", "r") as file:
        settings = json.load(file)

    return settings[setting]

def get_all_settings():
    with open("user_files/settings.json", "r") as file:
        settings = json.load(file)

    return settings

def set_setting(setting, value):
    # can both ADD and EDIT values in a dict so use this for both
    with open("user_files/settings.json", "r") as file:
        settings = json.load(file)

    settings[setting] = value

    with open("user_files/settings.json", "w") as file:
        json.dump(settings, file)

def delete_setting(setting):
    # can delete values in a dict
    with open("user_files/settings.json", "r") as file:
        settings = json.load(file)
        del settings[setting]

    with open("user_files/settings.json", "w") as file:
        json.dump(settings, file)

def check_valid():
    with open("user_files/settings.json", "r") as file:
        settings = json.load(file)

    if settings["valid"]:
        return True
    else:
        return False