from django.conf.urls import url
from .views import tic_tac_toe, computer_move

urlpatterns = [
    url(r'^$', tic_tac_toe, name='tic_tac_toe'),
    url(r'^computer_move/$', computer_move, name='computer_move'),
]