"""aquaponics_monitoring URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from mainpage import views as mainpage_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', mainpage_view.index),
    url(r'^admin/', admin.site.urls),
    url(r'^sensor_data/', include('sensor_data.urls')),
    url(r'^api/', include('rest_api.urls')),
    url(r'^supporting_apps/', include('supporting_apps.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
