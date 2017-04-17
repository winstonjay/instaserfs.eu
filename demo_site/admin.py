from django.contrib import admin
from .models import Post, Profile, DevOps


class PostAdmin(admin.ModelAdmin):
    list_display = ('message', 'intent', 'subjects', 'message_reply')
    list_display_links = ('message', 'intent', 'subjects', 'message_reply')

admin.site.register(Post, PostAdmin)

admin.site.register(Profile)


admin.site.register(DevOps)