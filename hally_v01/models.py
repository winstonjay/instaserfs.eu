# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save



from hally import Hally 

classifier = Hally()

# Create your models here.

class Subject(models.Model):
    noun = models.CharField(max_length=30, null=True, blank=True, unique=True)
    theKey = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.noun

    class Meta:
        ordering = ('noun',)




class Knowledge(models.Model):
    item_title = models.CharField(max_length=50)
    item_info = models.TextField()
    item_subjects =  models.ManyToManyField(Subject, blank=True)
    item_refs = models.CharField(max_length=500, null=True, blank=True)
    upload_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.item_title

    def __str__(self):
        return self.item_title




def sub_related_changed(sender, instance, *args, **kwargs):

    if instance.item_info:
        item_subjects = classifier.predict_subjects(instance.item_info)
        
        if item_subjects:
            to_update = []
            for sub in item_subjects:
                subject, created = Subject.objects.get_or_create(noun=sub, theKey=instance.item_title)
                to_update.append(subject)
            
            instance.item_subjects.add(*to_update)


            print instance.item_subjects.all()
    


def model_saved(sender, instance, *args, **kwargs):


        print instance




post_save.connect(sub_related_changed, sender=Knowledge)
m2m_changed.connect(model_saved, sender=Knowledge.item_subjects.through)


        