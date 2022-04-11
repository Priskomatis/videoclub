"""videoclub URL Configuration

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
from os import stat
from django.contrib import admin
from django.urls import path, include
from videoclubapp import views      #We import the views we created in our app.
from django.conf.urls.static import static
from django.conf import settings
from videoclubapp.views import ChangePasswordView

app_name="videoclubapp"



urlpatterns = [
    path('admin/', admin.site.urls),
    path('videoclubapp/', include('videoclubapp.urls')),  #This is the root url, anything I type after that is from the "videoclubapp.urls"
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]

#For storin Images I upload from the Admin Interface NEEDS WORK.

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)