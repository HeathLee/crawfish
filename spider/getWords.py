# -*-coding:utf-8 -*-

import re
import sys
import time
import math
import json
import logging
import requests
from bs4 import BeautifulSoup

# 配置日志模块，同时输出到屏幕和文件
logger = logging.getLogger('spider_logger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %('
                              'message)s')
fh = logging.FileHandler('spider.log')
sh = logging.StreamHandler()
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)

BASEURL = 'https://www.shanbay.com'
BOOKURL = 'https://www.shanbay.com/wordbook/6091/'

# 获取指定单词书中的分组
r = requests.get(BOOKURL)
if r.status_code != 200:
    logger.error('Get book failed')
    sys.exit(0)
logger.info('Get book succeeded')
soup = BeautifulSoup(r.text, 'lxml')
group_list = [item['href'] for item in
              soup.select('.wordbook-wordlist-name > a')]
time.sleep(5)

# 获取每个分组有多少页面
page_count = [math.ceil(int(re.search(r'\d+', item.text).group(0)) / 20) for
              item in soup.select('.wordbook-wordlist-count')]

for group_index in range(15, len(group_list)):
    for i in range(1, page_count[group_index] + 1):
        r = requests.get(BASEURL + group_list[group_index] + '?page=' + str(i))
        if r.status_code != 200:
            logger.error('Get %s failed' % r.url)
        else:
            logger.info('Get %s succeeded' % r.url)
            soup = BeautifulSoup(r.text, 'lxml')
            words = [item.text for item in soup.select('td strong')]
            definitions = [item.text for item in soup.select(
                'td.span10')]
            word_dict = {}
            with open('CET4.txt', 'a') as f:
                for j in range(len(words)):
                    word_dict[words[j]] = definitions[j]
                json.dump(word_dict, f, ensure_ascii=False)
            time.sleep(5)
