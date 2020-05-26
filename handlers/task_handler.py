import json
import sys
import os

def get_all_tasks():
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
    driver_path = os.path.join(application_path, 'user_files/tasks.json')
    with open(driver_path, "r") as file:
        tasks = json.load(file)

    return tasks

def get_task_at_index(index):
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
    driver_path = os.path.join(application_path, 'user_files/tasks.json')
    with open(driver_path, "r") as file:
        tasks = json.load(file)

    return tasks[index]

def get_num_tasks():
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
    driver_path = os.path.join(application_path, 'user_files/tasks.json')
    with open(driver_path, "r") as file:
        tasks = json.load(file)

    return len(tasks)

def insert_tasks(tasks):
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
        print("path", application_path)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
        application_path = application_path.split("/")
        application_path.remove(application_path[6])
        application_path.remove(application_path[0])
        appstr = '/'
        for char in application_path:
            appstr += char + '/'
        application_path = appstr
        print(application_path)
    driver_path = os.path.join(application_path, 'user_files/tasks.json')
    with open(driver_path, "w") as file:
        json.dump(tasks, file)

def get_tasks_as_string():
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
    driver_path = os.path.join(application_path, 'user_files/tasks.json')
    with open(driver_path, "r") as file:
        tasks = json.load(file)

    task_list = []

    for task in tasks:
        task_string = []
        index = 0
        for task_item in task:
            if index == 0 or index == 1:
                if len(task_item) > 19:
                    task_item = task_item[0:15] + '...'
                    task_string.append(task_item)
                else:
                    space = ''
                    for i in range(1, 19 - len(task_item)):
                        space += ' '
                    task_item += space
                    task_string.append(task_item)
            else:
                if len(task_item) > 14:
                    task_item = task_item[0:10] + '...'
                    task_string.append(task_item)
                else:
                    if task_item == 'True' or task_item == 'False':
                        pass
                    else:
                        space = ''
                        for i in range(1, 14 - len(task_item)):
                            space += ' '
                        task_item += space
                        task_string.append(task_item)
            index += 1
        task_list.append(task_string)

    return task_list
