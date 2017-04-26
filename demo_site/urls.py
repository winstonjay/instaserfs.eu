import os
from django.conf.urls import url
from .views import insta_home, landing_page, demo, logout_link, create_post

urlpatterns = [

    url(r'^$', insta_home, name='insta_home'),

    url(r'^extended_mind_demo/$', landing_page, name='landing_page'),

    url(r'^extended_mind_demo/'+os.environ.get("DEMO_URL")+r'/$', demo, name='demo'),

    url(r'^extended_mind_demo/logout/', logout_link, name="logout_link"),

    url(r'^extended_mind_demo/'+os.environ.get("CREATE_POST_URL")+r'/$', create_post, name='create_post'),
]

