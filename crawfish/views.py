from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict

import json
import requests
from bs4 import BeautifulSoup

from crawfish.models import *


@login_required
def index(request):
    can_start = request.user.current_level is not None
    return render(request, 'crawfish/index.html', {'can_start': can_start})


@login_required
@csrf_exempt
def set_level(request):
    if request.method == 'GET':
        return render(request, 'crawfish/set_level.html')

    if request.method == 'POST':
        try:
            level_name = request.POST.get('level', '')
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'code': 1}))

        if level_name == '':
            return HttpResponse(json.dumps({'code': 1}))

        try:
            level = Level.objects.get(name=level_name)
            user = request.user
            user.current_level = level.id
            user.save()
            return HttpResponse(json.dumps({'code': 0}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'code': 1}))


@login_required
@csrf_protect
def set_word_limit(request):
    if request.method == 'GET':
        return render(request, 'crawfish/set_word_limit.html')

    if request.method == 'POST':
        try:
            limit = request.POST.get('word_limit', '')
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'code': 1}))

        if limit == '':
            return HttpResponse(json.dumps({'code': 1}))

        try:
            limit = int(limit)
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'code': 1}))

        if limit not in [20, 50, 70, 100]:
            return HttpResponse(json.dumps({'code': 1}))

        try:
            request.user.word_limit = limit
            request.user.save()
            return render(request, 'crawfish/index.html')
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'code': 1}))


@login_required
def bdc(request):
    user = request.user
    user.today = 0
    level = Level.objects.get(pk=user.current_level)
    offset = model_to_dict(user)[level.name.lower() + '_offset']
    word_ids = LevelWord.objects.filter(level_id=level.id)[offset: user.word_limit]
    # Don't support
    # words = Word.objects.filter(pk__in=word_ids)
    words = []
    for word_id in word_ids:
        word = Word.objects.get(pk=word_id.word_id)
        words.append({'content': word.content, 'cn_definition': word.cn_definition})

    return render(request, 'crawfish/bdc.html', {'words': words})


# 一个问题，本来想在前端用ajax调用api来请求例句
# 但是扇贝不提供jsonp格式的调用，我解决不了跨域问题，sad
@login_required
def get_sentence(request):
    # 啊！爬数据的页面只提供了单词和中文释义，没有单词的ID
    # 拿例句就开始蛋疼了
    word = request.GET.get('word')
    data = requests.get('https://api.shanbay.com/bdc/search/?word=%s' % word)
    if data.status_code == 200:
        data = json.loads(data.text)
        # 例句的api不能用了啊啊啊啊
        # 只能爬页面然后分析了，这样页面写起来倒是简单了
        url = 'https://www.shanbay.com/bdc/vocabulary/%s/' % data['data']['id']
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'lxml')
            sentence = str(soup.select('#learning-examples-box')[0])
            return HttpResponse(json.dumps({'sentence': sentence}))


@login_required
def finished_today(request):
    user = request.user
    if hasattr(user, 'today'):
        if user.today == user.word_limit:
            level = Level.objects.get(pk=user.current_level).name.lower() + \
                    '_offset'
            setattr(user, level, getattr(user, level) + user.word_limit)
            user.save()

            return render(request, 'crawfish/finished_today.html')
