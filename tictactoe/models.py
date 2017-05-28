# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

OUTCOMES = (
    ("computer", "COMPUTER"),
    ("draws", "DRAWS"), 
    ("humans", "HUMANS")
)

class Counter(models.Model):
    title = models.CharField(max_length=30, choices=OUTCOMES)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

