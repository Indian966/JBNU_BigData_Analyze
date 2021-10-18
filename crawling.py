import io
import pandas as pd
import re
import time
import urllib.request
import datetime as dt

from bs4 import BeautifulSoup
from pandas import DataFrame
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

# def createURlList():
#     url_list = pd.read_csv('url_list.csv')
#     return url_list

# html 파싱
def parseHtml(url):
    num_of_pagedowns = 20
    wd = webdriver.Chrome()
    wd.implicitly_wait(0.1)


    wd.get(url)
    body = wd.find_element_by_tag_name('body')

    while num_of_pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
        num_of_pagedowns -= 1

    page_source = wd.page_source
    html = BeautifulSoup(page_source,'html.parser')

    return html

# 채널이름 찾기
def findChannelName(html):
    channel_name = html.find(id='text-container').text.strip()

    return channel_name

def crawllingQuery(html):
    query_list = []

    for table_row in html.find_all(id="video-title"):
        href = table_row.get('href')
        query = href[9:]
        query_list.append(query)

    return query_list

def createQueryListCsv(query_list,channel_name):
    query_list_dt = pd.DataFrame(query_list, columns=['query'])
    query_list_dt.to_csv(f"{channel_name}_queryList.csv", encoding='utf-8-sig', index=True)


# url_list = createURlList()

url = 'https://www.youtube.com/user/zilioner83/videos'

parse_html = parseHtml(url)
query_list = crawllingQuery(parse_html)
channel_name = findChannelName(parse_html)
