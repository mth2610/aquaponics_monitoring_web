from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^sites$', views.SiteList.as_view()),
    url(r'^datavalues$', views.DataValues.as_view()),
    url(r'^images$', views.ImageList.as_view()),
    url(r'^ipcameras$', views.IpCameras.as_view()),
    url(r'^ipcamera_controller$', views.IpCameraController.as_view()),
    url(r'^fishtanks$', views.FishTanks.as_view()),
    # url(r'^fishtanks/parameters$', views.FishTankParameters.as_view()),
    # url(r'^fishtanks/feedings$', views.FishTankFeeding.as_view()),
    # url(r'^fishtanks/fishdeath$', views.FishTanks.as_view()),
    # url(r'^fishtanks/manual_monitorings$', views.FishTanksManualMonitoring.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
