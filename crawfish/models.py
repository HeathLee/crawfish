# -*- coding:utf-8 -*-

import os
from django.db import models
from users.models import User


class Word(models.Model):
    id = models.AutoField(primary_key=True)
    # 英文释义
    en_definition = models.TextField()
    # 中文释义
    cn_definition = models.TextField(null=False)
    # 单词内容
    content = models.CharField(max_length=30, null=False, unique=True)
    # 音标
    pronunciation = models.CharField(max_length=30)
    # 发音url
    audio = models.TextField()
    # 创建时间
    ctime = models.DateTimeField(auto_now_add=True)
    # 修改时间
    mtime = models.DateTimeField(auto_now=True)
    # 扇贝id
    shanbay_id = models.IntegerField(null=True)
    remark = models.TextField(null=True)

    class Meta:
        db_table = 'words'


class Level(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False, unique=True)
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    remark = models.TextField()

    class Meta:
        db_table = 'levels'


class LevelWord(models.Model):
    id = models.AutoField(primary_key=True)
    level_id = models.IntegerField()
    word_id = models.IntegerField()

    class Meta:
        db_table = 'level_words'


class Note(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    word_id = models.IntegerField()
    user_name = models.CharField(max_length=30, null=True)
    content = models.TextField()
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    remark = models.TextField()

    class Meta:
        db_table = 'notes'
