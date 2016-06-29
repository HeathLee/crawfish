# -*- coding:utf-8 -*-

import os
from django.db import models

class Word(models.Model):
    id = models.AutoField(primary_key=True)
