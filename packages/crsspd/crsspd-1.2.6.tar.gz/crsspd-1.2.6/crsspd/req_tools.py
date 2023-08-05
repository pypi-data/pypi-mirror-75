import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def get_html(url,encode='utf-8',timeout=30,ssl_error=False):
    useragent = UserAgent(verify_ssl=False).random if ssl_error else UserAgent().random
    try:
        headers = {
            "User-Agent": useragent,
            "Connection": "close"
        }
        r = requests.get(url, timeout=timeout, headers=headers)
        r.encoding = encode
        if r.status_code != 200:
            r.raise_for_status()
        return r.text
    except requests.HTTPError:
        return ""

def crawl_url(url,encode='utf-8',selector='',save_path='',timeout=30,debug=False,ssl_error=False):
    html = get_html(url,encode=encode,timeout=timeout,ssl_error=ssl_error)
    if html:
        if debug: print(html)
        if selector:
            soup = BeautifulSoup(html, 'html.parser')
            find_soup = soup.select(selector)
            print('数据个数:', len(find_soup))
            for f in find_soup:
                name = f.text.strip() or ''
                href = f["href"] or ''
                if debug: print(name, href)
                if save_path:
                    with open(save_path, 'a', encoding='utf-8') as fw:
                        fw.write(href + ',' + name + '\n')
        else:
            return html
    else:
        print('网址错误，请检查.')

def post_api_url(url,data):
    r = requests.post(url, json = data, headers={"Connection": "close"})
    if r.status_code != 200:
        r.raise_for_status()
    return r.json()

def get_api_url(url):
    r = requests.get(url, headers={"Connection": "close"})
    if r.status_code != 200:
        r.raise_for_status()
    return r.json()
