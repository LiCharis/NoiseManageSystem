"""ManageSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views as managesystem_Views, settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ManageSystem/dashboard/', managesystem_Views.dashboard),
    path('car/', include('car.urls')),
    path('data/', include('data.urls')),
    path('loudness/', include('loudness.urls')),
    path('sharpness/', include('sharpness.urls')),
    path('volatility/', include('volatility.urls')),
    path('clarity/', include('clarity.urls')),
    path('user/', include('user.urls')),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)