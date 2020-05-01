import time
from selenium import webdriver
from threading import Thread
from multiprocessing.pool import ThreadPool


class ProxyTester:
    def __init__(self, port, ip):
        self.port = port
        self.ip = ip

    def test_proxy(self):
        PROXY = self.ip + ":" + self.port
        return_list = []
        try:
            start = time.time()
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
            chrome_options.add_argument('--headless')
            chrome = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')
            try:
                chrome.get("http://google.com")
                if chrome.title.lower() == 'google':
                    chrome.quit()
                    return_list.append(True)
                    return_list.append(time.time() - start)
                    return return_list
                else:
                    chrome.quit()
                    return_list.append(False)
                    return return_list
            except:
                return_list.append(False)
                return return_list
        except:
            return_list.append(False)
            return return_list


class ProxiesTester():
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
        # proxy_list = [["port", "ip], ["port", "ip], ["port", "ip]]

    def test_proxies(self, i):
        port = self.proxy_list[i][0]
        ip = self.proxy_list[i][1]
        PROXY = ip + ":" + port
        return_list = []
        try:
            start = time.time()
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
            chrome_options.add_argument('--headless')
            chrome = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')
            try:
                chrome.get("http://google.com")
                if chrome.title.lower() == 'google':
                    chrome.quit()
                    return_list.append(True)
                    return_list.append(time.time() - start)
                    return return_list
                else:
                    chrome.quit()
                    return_list.append(False)
                    return return_list
            except:
                return_list.append(False)
                return return_list
        except:
            return_list.append(False)
            return return_list

    def proxy_threads(self):
        threads = []
        results = []
        pool = ThreadPool(processes=len(self.proxy_list))
        for i in range(0, len(self.proxy_list)):
            async_result = pool.apply_async(self.test_proxies, (i,))
            threads.append(async_result)
        for e in range(0, len(self.proxy_list)):
            return_val = threads[e].get()
            results.append(return_val)
        return results

