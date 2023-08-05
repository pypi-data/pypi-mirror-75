from parser_libraries import functions as f
from parser_libraries import SQL as SQL
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time
import logging
import logging.handlers


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address='/dev/log')
formatter = logging.Formatter(f'%(module)s.{__name__}: %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

URL_COMMITTEE = 'http://duma.gov.ru/duma/commissions/'
HOST = 'http://www.gosduma.net'
chromedriver = SQL.get_con_info()[-1]


def parser():
    log.debug(f"The script {__name__} starts working")

    chromedriver = SQL.get_con_info()[-1]
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    browser.get(URL_COMMITTEE)
    time.sleep(6)
    ls = browser.find_elements_by_tag_name("li")
    for  l in ls:
        html = l.click()
    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.find_all('li', class_='list-persons__item ')
    print(soup)
    return [{'code': 2, 'script': os.path.basename(__file__)}]


parser()
