# howdy/urls.py
from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('fetch/', views.RUD_action),
    path('del/', views.RUD_action),
    path('modify/', views.RUD_action),
    #path('createlog/', views.create_action),
    path('createlog/', views.Actions.as_view()),
]