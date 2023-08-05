from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class SelenuimTools(object):
    def __init__(self,chrome_path='/Users/bappy/opt/chromedriver',headless=True):
        self.chrome_path=chrome_path
        self.headless=headless

    def get_proxy_by_selenium(self):
        chrome_driver = create_chrome_driver(self.chrome_path,headless=self.headless)
        proxy_list = []

        chrome_driver.get('http://proxylist.fatezero.org/')
        chrome_driver.implicitly_wait(5)

        trs = find_elements_by_css_selector(chrome_driver,'#table > tbody > tr')
        for tr in trs:
            host = find_element_by_css_selector(tr,'td:nth-child(1)').text
            port = find_element_by_css_selector(tr,'td:nth-child(2)').text
            type = find_element_by_css_selector(tr,'td:nth-child(3)').text
            if type == 'http':
                proxy_list.append(f'{host}:{port}')

        chrome_driver.quit()
        return proxy_list

    def get_html(self,url,wait_time=1,wait_show=''):
        try:
            chrome_driver = create_chrome_driver(self.chrome_path, headless=self.headless)
            chrome_driver.get(url)
            chrome_driver.implicitly_wait(10)

            if not wait_show:
                # 强制等待
                time.sleep(wait_time)
            else:
                # 显示等待ajax加载完成到div,返回div元素
                if wait_show[0] == '#':
                    WebDriverWait(chrome_driver, wait_time).until(
                        EC.presence_of_element_located((By.ID, wait_show[1:])))
                else:
                    WebDriverWait(chrome_driver, wait_time).until(
                        EC.presence_of_element_located((By.CLASS_NAME, wait_show)))

            js = "return document.documentElement.outerHTML"
            html = chrome_driver.execute_script(js)

            chrome_driver.quit()
            return html
        except:
            print("检查chrome版本，chrome://version/")
            print("下载最新chromedriver http://chromedriver.storage.googleapis.com/index.html")
            return ""

def find_element_by_css_selector(element, selector):
    try:
        return element.find_element_by_css_selector(selector)
    except:
        return None

def find_elements_by_css_selector(element, selector):
    try:
        return element.find_elements_by_css_selector(selector)
    except:
        return []

def create_chrome_driver(chrome_path,headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # http://npm.taobao.org/mirrors/chromedriver/

    driver = webdriver.Chrome(chrome_options=options,executable_path=chrome_path)
    driver.maximize_window()
    driver.implicitly_wait(30)
    return driver


if __name__ == '__main__':
    url='http://proxylist.fatezero.org/'
    selm=SelenuimTools()
    print(selm.get_html(url))
