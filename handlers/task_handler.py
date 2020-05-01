import json

def get_all_tasks():
    with open("user_files/tasks.json", "r") as file:
        tasks = json.load(file)

    return tasks

def get_task_at_index(index):
    with open("user_files/tasks.json", "r") as file:
        tasks = json.load(file)

    return tasks[index]

def get_num_tasks():
    with open("user_files/tasks.json", "r") as file:
        tasks = json.load(file)

    return len(tasks)

def insert_tasks(tasks):
    with open("user_files/tasks.json", "w") as file:
        json.dump(tasks, file)

def get_tasks_as_string():
    with open("user_files/tasks.json", "r") as file:
        tasks = json.load(file)

    task_list = []

    for task in tasks:
        task_string = []
        for task_item in task:
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
        task_list.append(task_string)

    return task_list
