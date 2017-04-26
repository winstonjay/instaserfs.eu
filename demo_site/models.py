from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


from hally_v01.hally import Hally 

classifier = Hally()

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    message = models.CharField(max_length=500)
    intent = models.CharField(max_length=30, null=True, blank=True)
    message_reply = models.CharField(max_length=500, null=True, blank=True)
    subjects = models.CharField(max_length=100, null=True, blank=True)
    upload_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.message

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['upload_date']


def pre_save_post_reciever(sender, instance, *args, **kwargs):
    if instance.message:
        
        intent = classifier.predict_intent(instance.message)
        subjects = classifier.predict_subjects(instance.message)

        instance.intent = intent
        instance.subjects = subjects
        instance.message_reply = classifier.decide_response(instance.message, intent, subjects)

pre_save.connect(pre_save_post_reciever, sender=Post)



class DevOps(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=30)
    info = models.TextField(null=True, blank=True)
    upload_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['upload_date']





# class Profile(models.Model):
#     author = models.OneToOneField(User, on_delete=models.CASCADE)    
#     bot_name = models.CharField(max_length=30, blank=True)
#     user_name = models.CharField(max_length=30, blank=True)



# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


