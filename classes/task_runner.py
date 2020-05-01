from shops.supreme import SupremeTShirt
from shops.supreme import SupremeAccessories
from shops.supreme import SupremeTopsSweaters
from shops.cactus_jack import CactusJack

class TaskRunner:
    def __init__(self, all_tasks, all_accounts, all_proxies):
        self.all_tasks = all_tasks
        self.all_accounts = all_accounts
        self.all_proxies = all_proxies

    def task_pool_executor(self):
        supreme_t_shirts_tasks = []
        supreme_t_shirts_accounts = []
        supreme_t_shirts_proxies = []

        supreme_accessories_tasks = []
        supreme_accessories_accounts = []
        supreme_accessories_proxies = []

        cactus_jack_tasks = []
        cactus_jack_accounts = []
        cactus_jack_proxies = []

        index = 0
        for task in self.all_tasks:
            if task[0] == 'Supreme (T-Shirts)': # shop
                supreme_t_shirts_tasks.append(task)
                supreme_t_shirts_accounts.append(self.all_accounts[index])
                supreme_t_shirts_proxies.append(self.all_proxies[index])
            if task[0] == 'Supreme (Accessories)':
                supreme_accessories_tasks.append(task)
                supreme_accessories_accounts.append(self.all_accounts[index])
                supreme_accessories_proxies.append(self.all_proxies[index])
            if task[0] == 'Supreme (Tops / Sweaters)':
                supreme_accessories_tasks.append(task)
                supreme_accessories_accounts.append(self.all_accounts[index])
                supreme_accessories_proxies.append(self.all_proxies[index])
            if task[0] == 'Cactus Jack':
                cactus_jack_tasks.append(task)
                cactus_jack_accounts.append(self.all_accounts[index])
                cactus_jack_proxies.append(self.all_proxies[index])
            index += 1

        if len(supreme_t_shirts_tasks) > 0: # if there are tasks
            supreme_tasks = SupremeTShirt(supreme_t_shirts_tasks, supreme_t_shirts_accounts)
            supreme_tasks.task_pool()
        if len(supreme_accessories_tasks) > 0:
            supreme_tasks = SupremeAccessories(supreme_accessories_tasks, supreme_accessories_accounts, supreme_accessories_proxies)
            supreme_tasks.task_pool()
        if len(cactus_jack_tasks) > 0:
            travisscott_tasks = CactusJack(cactus_jack_tasks, cactus_jack_accounts)
            travisscott_tasks.task_pool()
