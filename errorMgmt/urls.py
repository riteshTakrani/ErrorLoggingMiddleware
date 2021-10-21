# howdy/urls.py
from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('fetch/', views.Actions.as_view()),
    path('del/', views.Actions.as_view()),
    path('modify/', views.Actions.as_view()),
    path('createlog/', views.Actions.as_view()),
]