import sys
import os
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
from discord_webhook import DiscordWebhook

# the worker class that will house the supreme script
# and the worker class for supreme as well as send the signals

class WorkerSignals(QObject):
    searching = pyqtSignal() # i of task that is at this point
    found = pyqtSignal()
    cart = pyqtSignal()
    captcha = pyqtSignal()
    checkout = pyqtSignal()
    success = pyqtSignal(bool) # true if copped, false if not
    stopped = pyqtSignal()
    cart_error = pyqtSignal()
    captcha_error = pyqtSignal()
    card_declined = pyqtSignal()
    sold_out = pyqtSignal()
    restock = pyqtSignal()


class Worker():
    def __init__(self, num, tasks, accounts, proxies, url):
        super().__init__()
        self.num = num
        default_settings = settings_handler.get_all_settings()
        self.settings = [default_settings["safe mode"], default_settings["monitor delay"], default_settings["retry delay"]]
        self.tasks = tasks
        self.accounts = accounts
        self.proxies = proxies
        self.signals = WorkerSignals()
        self.signals.blockSignals(False)
        self.url = url
        self.safe_mode = self.settings[0]
        self.monitor_delay = self.settings[1]
        self.retry_delay = self.settings[2]
        self.terminate = False # if true, returns to end the thread


    def run_tasks(self):
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
        driver_path = os.path.join(application_path, 'chromedriver')
        print(driver_path)
        self.signals.blockSignals(False)
        if not self.terminate:
            self.product = self.tasks[self.num][1]
            self.size = self.tasks[self.num][2]
            self.delay = self.tasks[self.num][3]
            self.delay = self.delay[:-2]
            product_tags = self.product.split(' ')
            positive_tags = []
            negative_tags = []
            for tag in product_tags:
                if tag[:1] == '+':
                    positive_tags.append(tag[1:])
                else:
                    negative_tags.append(tag[1:])

            full_name = self.accounts[self.num][0] + ' ' + self.accounts[self.num][1]
            exp = self.accounts[self.num][9].split('/')
            exp_month = exp[0]
            exp_month = exp_month.replace('0', '')
            exp_year = exp[1]
            exp_year = '20' + exp_year

            if not self.terminate:
                found_product = False
                while not found_product:
                    if not self.terminate:
                        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.3112.50 Safari/537.36'
                        options = webdriver.ChromeOptions()
                        options.add_argument("--window-size=1920,1080")
                        options.add_argument("--start-maximized")
                        options.add_argument("--headless")
                        options.add_argument(f'user-agent={user_agent}')
                        if self.proxies[self.num] != False:
                            port = self.proxies[self.num][0]
                            ip = self.proxies[self.num][1]
                            PROXY = ip + ":" + port
                            options.add_argument('--proxy-server=http://%s' % PROXY)
                        driver = webdriver.Chrome(options=options, executable_path=driver_path)
                        driver.get(self.url)
                        links = driver.find_elements_by_xpath('//*[@id="container"]/li/div/a')
                        product_names = driver.find_elements_by_xpath('//*[@id="container"]/li/div/div[1]')
                        product_styles = driver.find_elements_by_xpath('//*[@id="container"]/li/div/div[2]')
                        if not self.terminate:
                            self.signals.searching.emit()
                            if not self.terminate:
                                for i in range(0, len(links)):
                                    pos_check = False
                                    full_product_name = product_names[i].text.lower() + ' ' + product_styles[i].text.lower()
                                    full_product_name = full_product_name.replace('\n', ' ')
                                    full_product_tags = full_product_name.split(' ')
                                    for tag in full_product_tags:
                                        try:
                                            new_split = tag.split('/')
                                            full_product_tags.remove(tag)
                                            for split_tag in new_split:
                                                full_product_tags.append(split_tag)
                                        except:  # no '/' in tag
                                            pass
                                    for positive_tag in positive_tags:
                                        if positive_tag.lower() in full_product_tags:
                                            pos_check = True
                                        else:
                                            pos_check = False
                                    neg_check = True
                                    for negative_tag in negative_tags:
                                        if negative_tag.lower() not in full_product_tags:
                                            neg_check = True
                                        else:
                                            neg_check = False
                                    if pos_check and neg_check:
                                        self.signals.found.emit()
                                        links[i].click()
                                        time.sleep(1)
                                        #select size
                                        if self.size != 'Random':
                                            all_sizes = Select(driver.find_element_by_xpath('//*[@id="s"]'))
                                            if self.size == 'S':
                                                all_sizes.select_by_value('Small')
                                            if self.size == 'M':
                                                all_sizes.select_by_value('Medium')
                                            if self.size == 'L':
                                                all_sizes.select_by_value('Large')
                                            if self.size == 'XL':
                                                all_sizes.select_by_value('XLarge')
                                        if self.safe_mode:
                                            time.sleep(1)
                                        driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').submit()
                                        if self.safe_mode:
                                            time.sleep(1)
                                        if not self.terminate:
                                            try:
                                                self.signals.cart.emit()
                                                driver.find_element_by_xpath('//*[@id="cart"]/a[2]').click()
                                                driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(full_name)  # name
                                                driver.find_element_by_xpath('//*[@id="order_email"]').send_keys(
                                                    self.accounts[self.num][2])  # email
                                                driver.find_element_by_xpath('//*[@id="order_tel"]').send_keys(
                                                    self.accounts[self.num][3])  # phone
                                                driver.find_element_by_xpath('//*[@id="bo"]').send_keys(self.accounts[self.num][4])  # address
                                                driver.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(
                                                    self.accounts[self.num][7])  # zip
                                                driver.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(
                                                    self.accounts[self.num][5])  # city
                                                driver.find_element_by_xpath('//*[@id="rnsnckrn"]').send_keys(
                                                    self.accounts[self.num][8])  # card number
                                                exp_month_elem = driver.find_element_by_xpath(
                                                    f'//*[@id="credit_card_month"]/option[{exp_month}]')  # exp month
                                                driver.execute_script("arguments[0].setAttribute('selected', arguments[1])", exp_month_elem,
                                                                      'selected')
                                                exp_year_elems = driver.find_elements_by_xpath('//*[@id="credit_card_year"]/option')
                                                for exp_choice in exp_year_elems:
                                                    if exp_choice.get_attribute('value') == exp_year:
                                                        driver.execute_script("arguments[0].setAttribute('selected', arguments[1])", exp_choice,
                                                                              'selected')  # exp year
                                                driver.find_element_by_xpath('//*[@id="orcer"]').send_keys(self.accounts[self.num][10])  # cvv
                                                # driver.find_element_by_xpath('//*[@id="order_terms"]').click() # checkbox
                                            except:
                                                self.signals.cart_error.emit()
                                            try:
                                                self.signals.captcha.emit()
                                                recaptcha = driver.find_element_by_xpath(
                                                    '//*[@id="cart-cc"]/fieldset/div[3]')  # deletes captcha #FUCKCAPTCHA
                                                driver.execute_script(
                                                    """
                                                    var element = arguments[0];
                                                    element.parentNode.removeChild(element);
                                                    """, recaptcha
                                                )
                                            except:
                                                self.signals.captcha_error.emit()
                                            self.signals.checkout.emit()
                                            time.sleep(float(int(self.delay)/1000))
                                            if not self.terminate:
                                                retry = True
                                                while retry:
                                                    try:
                                                        actions = ActionChains(driver)
                                                        actions.send_keys(Keys.TAB)
                                                        actions.send_keys(Keys.TAB)
                                                        actions.send_keys(Keys.ENTER)
                                                        actions.perform()
                                                        try:
                                                            confirmed = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="confirmation"]/p[1]'))).text
                                                            confirmed = confirmed.lower()
                                                            if 'thank you' in confirmed:
                                                            # if it says that product was copped, return true, if not return false
                                                                self.signals.success.emit(True)
                                                                retry = False
                                                                user = settings_handler.get_setting("webhook")
                                                                webhook = DiscordWebhook(url="https://discord.com/api/webhooks/711740619998887947/tidAheMHhsnXa5IQKR6MmoMV7jw9Xs4xbglcGJOxORjOhwsD2zGPnY-tNlcFo2cCdNaZ", content=f'User {user} copped {self.product} from Supreme!')
                                                                webhook.execute()
                                                            elif 'sold out' in confirmed:
                                                                self.signals.sold_out.emit()
                                                                time.sleep(1)
                                                            else:
                                                                self.signals.card_declined.emit()
                                                                time.sleep(1)
                                                            # tab, tab, enter submits the info
                                                            # found_product = True
                                                        except:
                                                            self.signals.success.emit(False)
                                                    except:
                                                        self.signals.restock.emit()
                                                        time.sleep(float(int(self.retry_delay)/1000))
                                                    else:
                                                        self.signals.success.emit(False)
                                            else:
                                                return
                                        else:
                                            return

                                else:
                                    time.sleep(float(int(self.monitor_delay)/1000))
                                    driver.quit()
                            else:
                                return
                        else:
                            return
                    else:
                        return
            else:
                return
        else:
            return

    @pyqtSlot()
    def kill_threads(self):
        self.signals.blockSignals(True)
        self.terminate = True
