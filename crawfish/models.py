# -*- coding:utf-8 -*-

import os
from django.db import models


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
    content = models.CharField(max_length=30, null=False)
    # 音标
    pronunciation = models.CharField(max_length=30)
    # 发音url
    audio = models.TextField()
    # 创建时间
    ctime = models.DateTimeField(auto_now_add=True)
    # 修改时间
    mtime = models.DateTimeField(auto_now=True)


# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     email = models.EmailField()
#     passwd = models.CharField(max_length=32)


