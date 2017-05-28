from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^overview/', views.overview, name='overview'),
    url(r'^details/', views.detail, name='detail'),
    #url(r'^details\.(?P<format>[a-z0-9]+)/?$', views.detail, name='detail'),
]
