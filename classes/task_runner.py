from shops.supreme import SupremeTShirt
from shops.supreme import SupremeAccessories
from shops.supreme import SupremeTopsSweaters
from shops.cactus_jack import CactusJack
from PyQt5.QtCore import *
from handlers import task_handler, account_handler, proxy_handler

# class TaskRunner:
#     def __init__(self, all_tasks, all_accounts, all_proxies):
#         self.all_tasks = all_tasks
#         self.all_accounts = all_accounts
#         self.all_proxies = all_proxies
#
#     def task_pool_executor(self):
#         supreme_t_shirts_tasks = []
#         supreme_t_shirts_accounts = []
#         supreme_t_shirts_proxies = []
#
#         supreme_accessories_tasks = []
#         supreme_accessories_accounts = []
#         supreme_accessories_proxies = []
#
#         index = 0
#         for task in self.all_tasks:
#             if task[0] == 'Supreme (T-Shirts)': # shop
#                 supreme_t_shirts_tasks.append(task)
#                 supreme_t_shirts_accounts.append(self.all_accounts[index])
#                 supreme_t_shirts_proxies.append(self.all_proxies[index])
#             if task[0] == 'Supreme (Accessories)':
#                 supreme_accessories_tasks.append(task)
#                 supreme_accessories_accounts.append(self.all_accounts[index])
#                 supreme_accessories_proxies.append(self.all_proxies[index])
#             index += 1
#
#         if len(supreme_t_shirts_tasks) > 0: # if there are tasks
#             supreme_tasks = SupremeTShirt(supreme_t_shirts_tasks, supreme_t_shirts_accounts)
#             supreme_tasks.task_pool()
#         if len(supreme_accessories_tasks) > 0:
#             supreme_tasks = SupremeAccessories(supreme_accessories_tasks, supreme_accessories_accounts, supreme_accessories_proxies)
#             supreme_tasks.task_pool())


class WorkerSignals(QObject):
    finished = pyqtSignal(list)
    result = pyqtSignal()
    # add more in-depth signals eventually, to specify whats happening


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def task_runner(self):
        self.all_tasks = task_handler.get_all_tasks()
        self.all_accounts = account_handler.get_all_accounts()
        self.all_proxies = proxy_handler.get_all_proxies()
        supreme_t_shirts_tasks = []
        supreme_t_shirts_accounts = []
        supreme_t_shirts_proxies = []

        supreme_accessories_tasks = []
        supreme_accessories_accounts = []
        supreme_accessories_proxies = []

        index = 0
        for task in self.all_tasks:
            if task[0] == 'Supreme (T-Shirts)':  # shop
                supreme_t_shirts_tasks.append(task)
                supreme_t_shirts_accounts.append(self.all_accounts[index])
                supreme_t_shirts_proxies.append(self.all_proxies[index])
            if task[0] == 'Supreme (Accessories)':
                supreme_accessories_tasks.append(task)
                supreme_accessories_accounts.append(self.all_accounts[index])
                supreme_accessories_proxies.append(self.all_proxies[index])
            index += 1

        if len(supreme_t_shirts_tasks) > 0:  # if there are tasks
            supreme_tasks = SupremeTShirt(supreme_t_shirts_tasks, supreme_t_shirts_accounts, supreme_t_shirts_proxies)
            supreme_tasks.task_pool()
        if len(supreme_accessories_tasks) > 0:
            supreme_tasks = SupremeAccessories(supreme_accessories_tasks, supreme_accessories_accounts, supreme_accessories_proxies)
            supreme_tasks.task_pool()

    @pyqtSlot(list)
    def run(self):
        self.signals.result.emit() # say processes started
        self.task_runner()