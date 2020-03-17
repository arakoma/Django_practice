from django.urls import path
from . import views


urlpatterns = [
    # rootURLに'post_list'という名前のviewを割り当てる
    path('', views.post_list, name='post_list'),
]