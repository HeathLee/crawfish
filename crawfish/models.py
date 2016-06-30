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
    # 熟悉度
    retention = models.IntegerField(default=0)
    # 学习度
    target_retention = models.IntegerField(default=5)
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
    remark = models.TextField()


class MyUser(User):
    cet4_offset = models.IntegerField()
    cet6_offset = models.IntegerField()
    ielts_offset = models.IntegerField()
    toefl_offset = models.IntegerField()
    word_limit = models.IntegerField(max_length=4, default=20)
    remark = models.TextField()


class Level(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False, unique=True)
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    remark = models.TextField()


class LevelWord(models.Model):
    id = models.AutoField(primary_key=True)
    level_id = models.IntegerField()
    word_id = models.IntegerField()


class Note(models.Model):
    id = models.AutoField(primary_key=True)
    word_id = models.IntegerField()
    content = models.TextField()
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    remark = models.TextField()
