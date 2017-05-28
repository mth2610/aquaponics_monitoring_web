from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^sites$', views.SiteList.as_view()),
    url(r'^datavalues$', views.DataValues.as_view()),
    url(r'^images$', views.ImageList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
