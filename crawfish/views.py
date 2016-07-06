from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.models import model_to_dict

import json
import logging
import requests
from bs4 import BeautifulSoup

from crawfish.models import *

logger=logging.getLogger("crawfish.views")


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
            logger.error('get level name failed')
            logger.error(e)
            return HttpResponse(json.dumps({'code': 1}))

        if level_name == '':
            return HttpResponse(json.dumps({'code': 1}))

        try:
            level = Level.objects.get(name=level_name)
            user = request.user
            user.current_level = level.id
            user.save()
            logger.info('set level succeeded')
            return HttpResponse(json.dumps({'code': 0}))
        except Exception as e:
            logger.error(e)
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
            logger.error('get word limit failed')
            logger.error(e)
            return HttpResponse(json.dumps({'code': 1}))

        if limit == '':
            logger.error('word limit is blank')
            return HttpResponse(json.dumps({'code': 1}))

        try:
            limit = int(limit)
        except Exception as e:
            logger.error('word limit is not int')
            logger.error(e)
            return HttpResponse(json.dumps({'code': 1}))

        if limit not in [20, 50, 70, 100]:
            return HttpResponse(json.dumps({'code': 1}))

        try:
            request.user.word_limit = limit
            request.user.save()
            logger.info('set word limit succeeded')
            return HttpResponseRedirect('/index')
        except Exception as e:
            logger.error(e)
            return HttpResponse(json.dumps({'code': 1}))


@login_required
def bdc(request):
    if request.user.current_level is None:
        return HttpResponseRedirect('/index/')

    user = request.user
    level = Level.objects.get(pk=user.current_level)
    offset = model_to_dict(user)[level.name.lower() + '_offset']

    # 完成一本书的学习
    if offset > LevelWord.objects.filter(level_id=level.id).count():
        return render(requests, 'crawfish/finished.html',
                      {'msg': '你已经完成本数的学习'})

    word_ids = LevelWord.objects.filter(level_id=level.id)[
               offset: offset + user.word_limit]

    words = []
    others_notes = []
    self_notes = []
    for word_id in word_ids:
        word = Word.objects.get(pk=word_id.word_id)
        words.append(
            {'content': word.content, 'cn_definition': word.cn_definition,
             'word_id': word.id, 'shanbay_id': word.shanbay_id})
        others_notes.append(list(map(model_to_dict, Note.objects.filter(
            word_id=word.id).exclude(user_id=user.id))))
        self_notes.append(list(map(model_to_dict,Note.objects.filter(
            word_id=word.id, user_id=user.id))))

    return render(request, 'crawfish/bdc.html', {'words': words,
                                                 'others_notes': others_notes,
                                                 'self_notes': self_notes})


# 一个问题，本来想在前端用ajax调用api来请求例句
# 但是扇贝不提供jsonp格式的调用，解决不了跨域问题，sad
@login_required
def get_sentence(request):
    try:
        shanbay_id = request.GET.get('shanbay_id', '')
        # 例句的api不能用
        # 只能爬页面然后分析了，这样页面写起来倒是简单了
        url = 'https://www.shanbay.com/bdc/vocabulary/%s/' % str(shanbay_id)
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'lxml')
            sentence = str(soup.select('#learning-examples-box')[0])
            if hasattr(request.user, 'today'):
                request.user.today += 1
            return HttpResponse(json.dumps({'sentence': sentence}))
    except Exception as e:
        logger.error(e)


@login_required
def finished_today(request):
    try:
        user = request.user
        level = Level.objects.get(pk=user.current_level).name.lower() + '_offset'
        setattr(user, level, getattr(user, level) + user.word_limit)
        user.save()
        return render(request, 'crawfish/finished.html',
                      {'msg': '你已经完成今天的学习'})
    except Exception as e:
        logger.error(e)


@login_required
@csrf_exempt
def add_note(request):
    word_id = request.POST.get('word_id', '')
    content = request.POST.get('content')
    user_id = request.user.id
    user_name = request.user.email.split('@')[0]

    note = Note()
    note.user_id = user_id
    note.word_id = word_id
    note.content = content
    note.user_name = user_name
    note.save()

    return HttpResponse(json.dumps({'code': 0, 'note': {'id': note.id,
                                                        'content': note.content}}))


@login_required
@csrf_exempt
def delete_note(request):
    note_id = request.POST.get('note_id', '')
    Note.objects.get(pk=note_id).delete()
    return HttpResponse(json.dumps({'code': 0, 'note_id': note_id}))

