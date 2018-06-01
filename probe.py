# coding:utf-8
import time, os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from libs import get_root_path

ext_dir_path = get_root_path('libs/crawler/chrome_ext')


def add_ext(options, crx_name):
    crx_path = ext_dir_path + crx_name + '.crx'
    if not os.path.isfile(crx_path):
        raise FileNotFoundError('没有这个插件')
    options.add_extension(crx_path)


def chrome_new_session(show_image=True, incognito=False, proxy_server=None, ua=None, mobile=False,
                       extensions=None):
    options = Options()

    if not show_image:
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

    if incognito:
        options.add_argument("--incognito")

    if ua:
        options.add_argument("user-agent=" + ua)

    if proxy_server:
        options.add_argument('--proxy-server=' + proxy_server)

    if mobile:  # todo 自由设定device name
        mobile_emulation = {"deviceName": "Google Nexus 5"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)

    if extensions:
        [add_ext(options, crx) for crx in extensions]

    return webdriver.Chrome(chrome_options=options)

def probe(page_url):
    open('out.txt','a').write('{"url":"%s"' % page_url.rstrip('\n'))
    driver = chrome_new_session(extensions=['wappalyzer'])
    driver.get(page_url)
    time.sleep(2)
    driver.quit()
    open('out.txt','a').write('}\n')


if __name__ == '__main__':
    urls = set()
    for link in open('urls.txt','r').readlines():
        urls.add(link.rstrip('\n'))
    print(urls)
    for url in urls:
        try:
            probe('http://'+url)
            probe('https://'+url)
        except:
            continue