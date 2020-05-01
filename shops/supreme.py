import time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class SupremeTShirt:
    def __init__(self, all_tasks, accounts_list):
        self.all_tasks = all_tasks
        self.accounts_list = accounts_list
        self.url = 'https://www.supremenewyork.com/shop/all/t-shirts'
        self.product = self.all_tasks[0][1]
        self.size = self.all_tasks[0][2]
        self.delay = 1000
        #self.account = ["Evan", "Brooks", 'evanbrooks0629@gmail.com', '5617898905', '6840 nw 65th terrrace', 'parkland', 'fl', '33067', '1111111111', '08/22', '111', 'evan brooks']
        # account_list[index] = ["evan", "brooks", "evanbrooks0629@gmail.com", "5617898905", "6840 nw 65th terrace", "parkland", "FL", "33067", "4737029082570848", "08/22", "035", "evan brooks", "6840 nw 65th terrace", "parkland", "FL", "33067"]
        # accounts_list[index] matches up perfectly ,so substitute it in

    def supreme_t_shirt(self, index):
        print(self.accounts_list[index])
        product_tags = self.product.split(' ')
        positive_tags = []
        negative_tags = []
        for tag in product_tags:
            if tag[:1] == '+':
                positive_tags.append(tag[1:])
            else:
                negative_tags.append(tag[1:])

        full_name = self.accounts_list[index][0] + ' ' + self.accounts_list[index][1]
        exp = self.accounts_list[index][9].split('/')
        exp_month = exp[0]
        exp_month = exp_month.replace('0', '')
        exp_year = exp[1]
        exp_year = '20' + exp_year
        print(exp_month)
        print(exp_year)

        found_product = False
        while not found_product:
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
            options = webdriver.ChromeOptions()
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            # options.add_argument("--headless")
            options.add_argument(f'user-agent={user_agent}')
            driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
            driver.get(self.url)
            start = time.time()
            links = driver.find_elements_by_xpath('//*[@id="container"]/li/div/a')
            product_names = driver.find_elements_by_xpath('//*[@id="container"]/li/div/div[1]')
            product_styles = driver.find_elements_by_xpath('//*[@id="container"]/li/div/div[2]')
            for i in range(0, len(links)):
                check = False
                full_product_name = product_names[i].text.lower() + ' ' + product_styles[i].text.lower()
                full_product_name = full_product_name.replace('\n', ' ')
                full_product_tags = full_product_name.split(' ')
                for tag in full_product_tags:
                    try:
                        new_split = tag.split('/')
                        full_product_tags.remove(tag)
                        for split_tag in new_split:
                            full_product_tags.append(split_tag)
                    except: # no '/' in tag
                        pass
                print(full_product_tags)
                for positive_tag in positive_tags:
                    if positive_tag.lower() in full_product_tags:
                        check = True
                    else:
                        check = False
                for negative_tag in negative_tags:
                    if negative_tag.lower() not in full_product_tags:
                        check = True
                    else:
                        check = False
                if check:
                    links[i].click()
                    time.sleep(1)
                    driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').submit()
                    time.sleep(1)
                    print('at cart')
                    driver.find_element_by_xpath('//*[@id="cart"]/a[2]').click()
                    driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(full_name)  # name
                    driver.find_element_by_xpath('//*[@id="order_email"]').send_keys(self.accounts_list[index][2])  # email
                    driver.find_element_by_xpath('//*[@id="order_tel"]').send_keys(self.accounts_list[index][3])  # phone
                    driver.find_element_by_xpath('//*[@id="bo"]').send_keys(self.accounts_list[index][4])  # address
                    driver.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(self.accounts_list[index][7])  # zip
                    driver.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(self.accounts_list[index][5])  # city
                    driver.find_element_by_xpath('//*[@id="rnsnckrn"]').send_keys(self.accounts_list[index][8])  # card number
                    exp_month_elem = driver.find_element_by_xpath(
                        f'//*[@id="credit_card_month"]/option[{exp_month}]')  # exp month
                    driver.execute_script("arguments[0].setAttribute('selected', arguments[1])", exp_month_elem,
                                          'selected')
                    exp_year_elems = driver.find_elements_by_xpath('//*[@id="credit_card_year"]/option')
                    for exp_choice in exp_year_elems:
                        print(exp_choice.get_attribute('value'))
                        if exp_choice.get_attribute('value') == exp_year:
                            driver.execute_script("arguments[0].setAttribute('selected', arguments[1])", exp_choice,
                                                  'selected')  # exp year
                    driver.find_element_by_xpath('//*[@id="orcer"]').send_keys(self.accounts_list[index][10])  # cvv
                    # driver.find_element_by_xpath('//*[@id="order_terms"]').click() # checkbox
                    recaptcha = driver.find_element_by_xpath(
                        '//*[@id="cart-cc"]/fieldset/div[3]')  # deletes captcha #FUCKCAPTCHA
                    driver.execute_script(
                        """
                        var element = arguments[0];
                        element.parentNode.removeChild(element);
                        """, recaptcha
                    )
                    time.sleep(self.delay / 1000)
                    actions = ActionChains(driver)
                    actions.send_keys(Keys.TAB)
                    actions.send_keys(Keys.TAB)
                    actions.send_keys(Keys.ENTER)
                    actions.perform()
                    print('copped')
                    print(time.time() - start)
                    # tab, tab, enter submits the info
                    # found_product = True

            else:
                driver.refresh()

    def task_pool(self):
        workers = []
        for i in range(0, len(self.all_tasks)):
            thread = Thread(target = self.supreme_t_shirt, args=[i])
            workers.append(thread)
        start = time.time()
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join()

        print(time.time() - start)


class SupremeAccessories:
    def __init__(self, all_tasks, accounts_list, proxies):
        self.proxies = proxies
        self.all_tasks = all_tasks
        self.accounts_list = accounts_list
        self.url = 'https://www.supremenewyork.com/shop/all/accessories'
        self.product = self.all_tasks[0][1]
        self.size = self.all_tasks[0][2]
        self.delay = 1000
        #self.account = ["Evan", "Brooks", 'evanbrooks0629@gmail.com', '5617898905', '6840 nw 65th terrrace', 'parkland', 'fl', '33067', '4737029082570848', '08/22', '035', 'evan brooks']
        # account_list[index] = ["evan", "brooks", "evanbrooks0629@gmail.com", "5617898905", "6840 nw 65th terrace", "parkland", "FL", "33067", "4737029082570848", "08/22", "035", "evan brooks", "6840 nw 65th terrace", "parkland", "FL", "33067"]
        # accounts_list[index] matches up perfectly ,so substitute it in

    def supreme_accessories(self, index):
        print(self.accounts_list[index])
        product_tags = self.product.split(' ')
        positive_tags = []
        negative_tags = []
        for tag in product_tags:
            if tag[:1] == '+':
                positive_tags.append(tag[1:])
            else:
                negative_tags.append(tag[1:])

        port = self.proxies[index][0]
        ip = self.proxies[index][1]
        PROXY = ip + ":" + port

        full_name = self.accounts_list[index][0] + ' ' + self.accounts_list[index][1]
        exp = self.accounts_list[index][9].split('/')
        exp_month = exp[0]
        exp_month = exp_month.replace('0', '')
        exp_year = exp[1]
        exp_year = '20' + exp_year
        print(exp_month)
        print(exp_year)

        found_product = False
        while not found_product:
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
            options = webdriver.ChromeOptions()
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            #options.add_argument('--proxy-server=http://%s' % PROXY)
            # options.add_argument("--headless")
            options.add_argument(f'user-agent={user_agent}')
            driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
            driver.get(self.url)
            start = time.time()
            links = driver.find_elements_by_xpath('//*[@id="container"]/li/div/a')
            product_names = driver.find_elements_by_xpath('//*[@id="container"]/li/div/div[1]')
            product_styles = driver.find_elements_by_xpath('//*[@id="container"]/li/div/div[2]')
            for i in range(0, len(links)):
                check = False
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
                print(full_product_tags)
                for positive_tag in positive_tags:
                    if positive_tag.lower() in full_product_tags:
                        check = True
                    else:
                        check = False
                for negative_tag in negative_tags:
                    if negative_tag.lower() not in full_product_tags:
                        check = True
                    else:
                        check = False
                if check:
                    links[i].click()
                    time.sleep(1)
                    driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').submit()
                    time.sleep(1)
                    print('at cart')
                    driver.find_element_by_xpath('//*[@id="cart"]/a[2]').click()
                    driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(full_name)  # name
                    driver.find_element_by_xpath('//*[@id="order_email"]').send_keys(
                        self.accounts_list[index][2])  # email
                    driver.find_element_by_xpath('//*[@id="order_tel"]').send_keys(
                        self.accounts_list[index][3])  # phone
                    driver.find_element_by_xpath('//*[@id="bo"]').send_keys(self.accounts_list[index][4])  # address
                    driver.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(
                        self.accounts_list[index][7])  # zip
                    driver.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(
                        self.accounts_list[index][5])  # city
                    driver.find_element_by_xpath('//*[@id="rnsnckrn"]').send_keys(
                        self.accounts_list[index][8])  # card number
                    exp_month_elem = driver.find_element_by_xpath(
                        f'//*[@id="credit_card_month"]/option[{exp_month}]')  # exp month
                    driver.execute_script("arguments[0].setAttribute('selected', arguments[1])", exp_month_elem,
                                          'selected')
                    exp_year_elems = driver.find_elements_by_xpath('//*[@id="credit_card_year"]/option')
                    for exp_choice in exp_year_elems:
                        print(exp_choice.get_attribute('value'))
                        if exp_choice.get_attribute('value') == exp_year:
                            driver.execute_script("arguments[0].setAttribute('selected', arguments[1])", exp_choice,
                                                  'selected')  # exp year
                    driver.find_element_by_xpath('//*[@id="orcer"]').send_keys(self.accounts_list[index][10])  # cvv
                    # driver.find_element_by_xpath('//*[@id="order_terms"]').click() # checkbox
                    recaptcha = driver.find_element_by_xpath(
                        '//*[@id="cart-cc"]/fieldset/div[3]')  # deletes captcha #FUCKCAPTCHA
                    driver.execute_script(
                        """
                        var element = arguments[0];
                        element.parentNode.removeChild(element);
                        """, recaptcha
                    )
                    time.sleep(self.delay / 1000)
                    actions = ActionChains(driver)
                    actions.send_keys(Keys.TAB)
                    actions.send_keys(Keys.TAB)
                    actions.send_keys(Keys.ENTER)
                    actions.perform()
                    print('copped')
                    print(time.time() - start)
                    # tab, tab, enter submits the info
                    # found_product = True

            else:
                driver.refresh()


    def task_pool(self):
        workers = []
        for i in range(0, len(self.all_tasks)):
            thread = Thread(target = self.supreme_accessories, args = [i])
            workers.append(thread)
        start = time.time()
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join()

        print(time.time() - start)


class SupremeTopsSweaters:
    def __init__(self, all_tasks, accounts_list, proxies):
        self.proxies = proxies
        self.all_tasks = all_tasks
        self.accounts_list = accounts_list
        self.url = 'https://www.supremenewyork.com/shop/all/tops_sweaters'
        self.product = self.all_tasks[0][1]
        self.size = self.all_tasks[0][2]
        self.delay = 1000

    def supreme_tops_sweaterss(self, index):
        print(self.accounts_list[index])
        product_tags = self.product.split(' ')
        positive_tags = []
        negative_tags = []
        for tag in product_tags:
            if tag[:1] == '+':
                positive_tags.append(tag[1:])
            else:
                negative_tags.append(tag[1:])

        port = self.proxies[index][0]
        ip = self.proxies[index][1]
        PROXY = ip + ":" + port

        full_name = self.accounts_list[index][0] + ' ' + self.accounts_list[index][1]
        exp = self.accounts_list[index][9].split('/')
        exp_month = exp[0]
        exp_month = exp_month.replace('0', '')
        exp_year = exp[1]
        exp_year = '20' + exp_year
        print(exp_month)
        print(exp_year)

        found_product = False
        while not found_product:
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
            options = webdriver.ChromeOptions()
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            options.add_argument('--proxy-server=http://%s' % PROXY)
            # options.add_argument("--headless")
            options.add_argument(f'user-agent={user_agent}')
            driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
            driver.get(self.url)
            start = time.time()
            links = driver.find_elements_by_xpath('//*[@id="container"]/li/div/a')
            product_names = driver.find_elements_by_xpath('//*[@id="container"]/li/div/div[1]')
            product_styles = driver.find_elements_by_xpath('//*[@id="container"]/li/div/div[2]')
            for i in range(0, len(links)):
                check = False
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
                print(full_product_tags)
                for positive_tag in positive_tags:
                    if positive_tag.lower() in full_product_tags:
                        check = True
                    else:
                        check = False
                for negative_tag in negative_tags:
                    if negative_tag.lower() not in full_product_tags:
                        check = True
                    else:
                        check = False
                if check:
                    links[i].click()
                    time.sleep(1)
                    driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').submit()
                    time.sleep(1)
                    print('at cart')
                    driver.find_element_by_xpath('//*[@id="cart"]/a[2]').click()
                    driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(full_name)  # name
                    driver.find_element_by_xpath('//*[@id="order_email"]').send_keys(
                        self.accounts_list[index][2])  # email
                    driver.find_element_by_xpath('//*[@id="order_tel"]').send_keys(
                        self.accounts_list[index][3])  # phone
                    driver.find_element_by_xpath('//*[@id="bo"]').send_keys(self.accounts_list[index][4])  # address
                    driver.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(
                        self.accounts_list[index][7])  # zip
                    driver.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(
                        self.accounts_list[index][5])  # city
                    driver.find_element_by_xpath('//*[@id="rnsnckrn"]').send_keys(
                        self.accounts_list[index][8])  # card number
                    exp_month_elem = driver.find_element_by_xpath(
                        f'//*[@id="credit_card_month"]/option[{exp_month}]')  # exp month
                    driver.execute_script("arguments[0].setAttribute('selected', arguments[1])", exp_month_elem,
                                          'selected')
                    exp_year_elems = driver.find_elements_by_xpath('//*[@id="credit_card_year"]/option')
                    for exp_choice in exp_year_elems:
                        print(exp_choice.get_attribute('value'))
                        if exp_choice.get_attribute('value') == exp_year:
                            driver.execute_script("arguments[0].setAttribute('selected', arguments[1])", exp_choice,
                                                  'selected')  # exp year
                    driver.find_element_by_xpath('//*[@id="orcer"]').send_keys(self.accounts_list[index][10])  # cvv
                    # driver.find_element_by_xpath('//*[@id="order_terms"]').click() # checkbox
                    recaptcha = driver.find_element_by_xpath(
                        '//*[@id="cart-cc"]/fieldset/div[3]')  # deletes captcha #FUCKCAPTCHA
                    driver.execute_script(
                        """
                        var element = arguments[0];
                        element.parentNode.removeChild(element);
                        """, recaptcha
                    )
                    time.sleep(self.delay / 1000)
                    actions = ActionChains(driver)
                    actions.send_keys(Keys.TAB)
                    actions.send_keys(Keys.TAB)
                    actions.send_keys(Keys.ENTER)
                    actions.perform()
                    print('copped')
                    print(time.time() - start)
                    # tab, tab, enter submits the info
                    # found_product = True

            else:
                driver.refresh()


    def task_pool(self):
        workers = []
        for i in range(0, len(self.all_tasks)):
            thread = Thread(target = self.supreme_tops_sweaterss, args = [i])
            workers.append(thread)
        start = time.time()
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join()

        print(time.time() - start)