"""Bluedit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from blueditUser import views
from subBluedit.views import showHome

urlpatterns = [
    path('', include('django.contrib.auth.urls'), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('admin/', admin.site.urls),
    # Home
    path('', showHome, name='home-feed'),
    # User-Path
    path('u/', include('blueditUser.urls'), name='users'),
    # Sub-Path
    path('b/', include('subBluedit.urls'), name='subs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()