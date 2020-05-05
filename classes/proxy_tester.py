import time
import sys
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread
from multiprocessing.pool import ThreadPool
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from handlers import proxy_handler


class WorkerSignals(QObject):
    finished = pyqtSignal(list)
    result = pyqtSignal()


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def proxy_test(self, i):
        self.proxy_list = proxy_handler.get_all_proxies()
        port = self.proxy_list[i][0]
        ip = self.proxy_list[i][1]
        PROXY = ip + ":" + port
        return_list = []
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
            chrome_options.add_argument('--headless')
            chrome = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')
            try:
                chrome.get("http://ping-test.net/mobile/speed_test")
                WebDriverWait(chrome, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="tester"]/div[1]'))
                ).click()
                time.sleep(10)
                speed = WebDriverWait(chrome, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="tester"]/div[12]/div[2]/span[1]'))
                )
                speed = int(speed.text)
                if speed:
                    chrome.quit()
                    return_list.append(True)
                    return_list.append(speed)
                    return_list.append(i)
                    return return_list
                else:
                    chrome.quit()
                    return_list.append(False)
                    return_list.append(i)
                    return return_list
            except:
                return_list.append(False)
                return_list.append(i)
                return return_list
        except:
            return_list.append(False)
            return_list.append(i)
            return return_list

    @pyqtSlot(list)
    def run(self):
        self.signals.result.emit()
        self.all_proxies = proxy_handler.get_proxy(*self.args)
        result = self.proxy_test(*self.args)
        self.signals.finished.emit(result)