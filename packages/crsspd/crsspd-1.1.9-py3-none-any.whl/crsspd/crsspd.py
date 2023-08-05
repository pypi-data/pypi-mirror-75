from crsspd.req_tools import *
from crsspd.selm_tools import SelenuimTools

class SpiderTools():
    def __init__(self,chrome_path='/Users/bappy/opt/chromedriver',headless=True):
        self.selm=SelenuimTools(chrome_path=chrome_path,headless=headless)

    def request(self):
        pass

    def selenuim(self):
        pass

    def scrapy(self):
        pass

    def splash(self):
        pass

    def get_url(self,url,dynamic=False,wait_time=1,wait_show='',ssl_error=False):
        if not dynamic:
            return get_html(url,ssl_error=ssl_error)
        else:
            return self.selm.get_html(url,wait_time=wait_time,wait_show=wait_show)

    def get_proxy(self):
        proxy_list=self.selm.get_proxy_by_selenium()
        return proxy_list

if __name__ == '__main__':
    import tempfile
    print(tempfile.gettempdir())
    # url='http://proxylist.fatezero.org/'
    url='http://www.anzhi.com/sort_50_1_hot.html'

    spd = SpiderTools()
    html=spd.get_url(url,dynamic=False,wait_time=10,ssl_error=False)
    print(html)


