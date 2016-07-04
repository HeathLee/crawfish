# -*-coding:utf8-*-

import requests
import json
import time
import sys
import os

sys.path.append('/home/heath/PycharmProjects/crawfish')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawfish.settings")

import django

django.setup()

from crawfish.models import Word
from django.db import transaction

count = 1903
all = Word.objects.all().count()
words = Word.objects.all()[count:]

while count < all:
    for word in words:
        resp = requests.get(
            'http://api.shanbay.com/bdc/search/?word=%s' % word.content,
            proxies={'http': '106.120.183.121:81'})
        if resp.status_code == 200:
            data = json.loads(resp.text)
            if data['status_code'] == 0:
                try:
                    word.shanbay_id = data['data']['id']
                    if data['data']['has_audio']:
                        word.audio = data['data']['audio']
                    if data['data']['en_definition']:
                        word.en_definition = data['data']['en_definition'][
                            'defn']
                    word.pronunciation = data['data']['pron']
                    word.save()
                    # time.sleep(1)
                    count += 1
                    print('succeed ' + str(count) + ' ' + word.content)
                except Exception as e:
                    print(word.content + ' failed')
                    print(data)
                    print(e)
                    sys.exit()
            else:
                print(word.content + 'failed')
                print(data)
                sys.exit()
        else:
            print(word.content + 'failed')
            print(resp.text)
            sys.exit()
