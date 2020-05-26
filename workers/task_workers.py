import sys
import traceback
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from threading import Thread
from multiprocessing.pool import ThreadPool
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from handlers import task_handler, account_handler, proxy_handler, settings_handler
from workers.supreme_workers import Worker as Supreme
from workers.supreme_workers import WorkerSignals as SupremeAccessoriesWorkerSignals

# the worker class that will house the supreme script
# and the worker class for supreme as well as send the signals

class WorkerSignals(QObject):
    started = pyqtSignal() # called at the beginning
    started_ind = pyqtSignal(int) # called at the beginning
    searching = pyqtSignal(int) # i of task that is at this point
    found = pyqtSignal(int)
    cart = pyqtSignal(int)
    captcha = pyqtSignal(int)
    checkout = pyqtSignal(int)
    success = pyqtSignal(int, bool) # true if copped, false if not
    stopped = pyqtSignal()
    stopped_ind = pyqtSignal(int)
    cart_error = pyqtSignal(int)
    captcha_error = pyqtSignal(int)
    card_declined = pyqtSignal(int)
    sold_out = pyqtSignal(int)
    restock = pyqtSignal(int)



class Worker(QRunnable):
    def __init__(self, is_running_all, num, tasks, accounts, proxies):
        super(Worker, self).__init__()
        self.is_running_all = is_running_all
        self.num = num
        self.tasks = tasks
        self.accounts = accounts
        self.proxies = proxies
        self.signals = WorkerSignals()
        self.methods = []

    def set_task(self, shop_name, i):
        if shop_name == 'Supreme (Accessories)':
            task = Supreme(i, self.tasks, self.accounts, self.proxies, 'https://www.supremenewyork.com/shop/all/accessories')
        if shop_name == 'Supreme (Shirts)':
            task = Supreme(i, self.tasks, self.accounts, self.proxies, 'https://www.supremenewyork.com/shop/all/shirts')
        if shop_name == 'Supreme (Shorts)':
            task = Supreme(i, self.tasks, self.accounts, self.proxies, 'https://www.supremenewyork.com/shop/all/shorts')
        if shop_name == 'Supreme (Pants)':
            task = Supreme(i, self.tasks, self.accounts, self.proxies, 'https://www.supremenewyork.com/shop/all/pants')
        if shop_name == 'Supreme (Sweatshirts)':
            task = Supreme(i, self.tasks, self.accounts, self.proxies, 'https://www.supremenewyork.com/shop/all/sweatshirts')
        if shop_name == 'Supreme (Bags)':
            task = Supreme(i, self.tasks, self.accounts, self.proxies, 'https://www.supremenewyork.com/shop/all/bags')
        if shop_name == 'Supreme (Hats)':
            task = Supreme(i, self.tasks, self.accounts, self.proxies, 'https://www.supremenewyork.com/shop/all/hats')
        if shop_name == 'Supreme (Jackets)':
            task = Supreme(i, self.tasks, self.accounts, self.proxies, 'https://www.supremenewyork.com/shop/all/jackets')
        if shop_name == 'Supreme (Skate)':
            task = Supreme(i, self.tasks, self.accounts, self.proxies, 'https://www.supremenewyork.com/shop/all/skate')
        if shop_name == 'Supreme (Tops / Sweaters)':
            task = Supreme(i, self.tasks, self.accounts, self.proxies, 'https://www.supremenewyork.com/shop/all/tops_sweaters')
        if shop_name == 'Supreme (Shoes)':
            task = Supreme(i, self.tasks, self.accounts, self.proxies, 'https://www.supremenewyork.com/shop/all/shoes')
        if shop_name == 'Supreme (T-Shirts)':
            task = Supreme(i, self.tasks, self.accounts, self.proxies, 'https://www.supremenewyork.com/shop/all/t-shirts')

        self.methods.append(task)
        task.signals.searching.connect(lambda: self.send_searching(i))
        task.signals.found.connect(lambda: self.send_found(i))
        task.signals.cart.connect(lambda: self.send_cart(i))
        task.signals.captcha.connect(lambda: self.send_captcha(i))
        task.signals.checkout.connect(lambda: self.send_checkout(i))
        task.signals.success.connect(lambda: self.send_success(i))
        task.signals.cart_error.connect(lambda: self.send_cart_error(i))
        task.signals.captcha_error.connect(lambda: self.send_captcha_error(i))
        task.signals.card_declined.connect(lambda: self.send_card_declined(i))
        task.signals.sold_out.connect(lambda: self.send_sold_out(i))
        task.signals.restock.connect(lambda: self.send_restock(i))
        task.run_tasks()



    def stop_task(self, is_stopping_all, i):
        if is_stopping_all:
            self.signals.stopped.emit()
            for method in self.methods:
                method.kill_threads()
        else:
            if len(self.methods) > 1:
                self.signals.stopped_ind.emit(i) # keep that it emits to the right signal

                self.methods[i].kill_threads() # i doesnt represent the number in terms of running tasks
            else:
                self.signals.stopped_ind.emit(i)  # keep that it emits to the right signal

                self.methods[0].kill_threads()
            # index = 0
            # for method in self.methods:
            #     print(method)
            #     if index == i:
            #         method.kill_threads()
            #         break
            #     else:
            #         pass
            #     index += 1


    @pyqtSlot(int)
    def send_searching(self, index):
        self.signals.searching.emit(index)

    @pyqtSlot(int)
    def send_found(self, index):
        self.signals.found.emit(index)

    @pyqtSlot(int)
    def send_cart(self, index):
        self.signals.cart.emit(index)

    @pyqtSlot(int)
    def send_captcha(self, index):
        self.signals.captcha.emit(index)

    @pyqtSlot(int)
    def send_checkout(self, index):
        self.signals.checkout.emit(index)

    @pyqtSlot(int, bool)
    def send_success(self, index, is_success):
        try:
            if index / 1 == index:
                self.signals.success.emit(index, is_success)
        except:
            self.signals.success.emit(index, is_success)

    @pyqtSlot(int)
    def send_cart_error(self, index):
        self.signals.cart_error.emit(index)

    @pyqtSlot(int)
    def send_captcha_error(self, index):
        self.signals.captcha_error.emit(index)

    @pyqtSlot(int)
    def send_card_declined(self, index):
        self.signals.card_declined.emit(index)

    @pyqtSlot(int)
    def send_sold_out(self, index):
        self.signals.sold_out.emit(index)

    @pyqtSlot(int)
    def send_restock(self, index):
        self.signals.restock.emit(index)


    @pyqtSlot()
    def run(self):
        if self.is_running_all:
            self.signals.started.emit()
            self.workers = []
            for i in range(len(self.tasks)):
                thread = Thread(target=self.set_task, args=[self.tasks[i][0], i])
                self.workers.append(thread)
            for worker in self.workers:
                worker.start()
            for worker in self.workers:
                worker.join()
        else:
            self.signals.started_ind.emit(self.num)
            self.worker = Thread(target=self.set_task, args=[self.tasks[self.num][0], self.num])
            self.worker.start()
            self.worker.join()
