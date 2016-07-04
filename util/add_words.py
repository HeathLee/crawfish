# -*-coding:utf8-*-

import json
import sys
import os

sys.path.append('/home/heath/PycharmProjects/crawfish')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawfish.settings")

import django
django.setup()

from crawfish.models import Word, Level, LevelWord
from django.db import transaction

with open('spider/IELTS.json', 'r') as f:
    data = json.load(f)
    level = Level.objects.get(name='IELTS')
    with transaction.atomic():
        for key, value in data.items():
            obj, created = Word.objects.get_or_create(content=key, defaults={
                'cn_definition': value})
            LevelWord.objects.create(level_id=level.id, word_id=obj.id)
