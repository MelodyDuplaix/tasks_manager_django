"""
URL configuration for manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin  # type: ignore
from django.urls import path, include  # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('password_change/', include('tasks.urls.accounts'), name='password_change'),
    path('accounts/', include('tasks.urls.accounts'), name='accounts'),
    path('', include('tasks.urls.views'), name='home'),
    path('submanager/', include('tasks.urls.submanager'), name='submanager'),
    path('tasks/', include('tasks.urls.tasks'), name='tasks'),
    path('rewards/', include('tasks.urls.rewards'), name='rewards'),
    path('statistics/', include('tasks.urls.statistics'), name='statistics'),
    path('types/', include('tasks.urls.type'), name='types'),
]
