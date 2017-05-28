from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^count_circles/', views.count_circles, name='count_circles'),
]
