from django.contrib import admin
from .models import Post, DevOps #,  Profile


class PostAdmin(admin.ModelAdmin):
    list_display = ('message', 'intent', 'subjects', 'message_reply', 'author')
    list_display_links = ('message', 'intent', 'subjects', 'message_reply', 'author')

admin.site.register(Post, PostAdmin)

# admin.site.register(Profile)


admin.site.register(DevOps)