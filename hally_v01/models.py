# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save

from hally import Hally 

classifier = Hally()

# Create your models here.

class Knowledge(models.Model):
    item_title = models.CharField(max_length=50)
    item_info = models.TextField()
    item_subjects = models.CharField(max_length=500, null=True, blank=True)
    item_refs = models.CharField(max_length=500, null=True, blank=True)
    upload_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.item_title

    def __str__(self):
        return self.item_title



def pre_save_knowledge_reciever(sender, instance, *args, **kwargs):
    if instance.item_info:
        item_subjects = classifier.predict_subjects(instance.item_info)

        if item_subjects == "":
            item_subjects = "fail"
        instance.item_subjects = item_subjects

pre_save.connect(pre_save_knowledge_reciever, sender=Knowledge)


        