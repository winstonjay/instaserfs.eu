# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from django.db import models
from django.db.models.signals import post_save
from django.db.models import Sum


OUTCOMES = (
    ("computer", "COMPUTER"),
    ("draws", "DRAWS"), 
    ("humans", "HUMANS")
)

class Counter(models.Model):
    title = models.CharField(max_length=30, choices=OUTCOMES)
    count = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(default=0.00)

    def __str__(self):
        return self.title


def update_percentages(sender, instance, *args, **kwargs):
    total_games = sender.objects.aggregate(Sum('count'))
    percentile = 100 / total_games['count__sum']
    for item in sender.objects.all():
        p = round(percentile * item.count, 2)
        if item.percentage != p: 
            item.percentage = p
            item.save()

post_save.connect(update_percentages, sender=Counter)

