# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Counter

class CountAdmin(admin.ModelAdmin):
    list_display = ('title', 'count')

admin.site.register(Counter, CountAdmin)