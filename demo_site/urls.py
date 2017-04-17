import os
from django.conf.urls import url
from .views import landing_page, demo, logout_link, create_post

urlpatterns = [
    url(r'^$', landing_page, name='landing_page'),

    url(r'^demo/'+os.environ.get("DEMO_URL")+r'/$', demo, name='demo'),

    url(r'^logout/', logout_link, name="logout_link"),

    url(r'^demo/'+os.environ.get("CREATE_POST_URL")+r'/$', create_post, name='create_post'),
]

