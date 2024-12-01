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
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.options, name='home'),
    path('update_submanager/<int:submanager_id>/', views.update_submanager, name='update_submanager'),
    path('add_submanager/', views.add_submanager, name='add_submanager'),
    path('delete_submanager/<int:submanager_id>', views.delete_submanager, name='delete_submanager'),
    path('<int:submanager_id>/', views.submanager_page, name='submanager_page'),
    path('action/<int:task_id>', views.task_action, name='task_action'),
    path('reward/<int:reward_id>', views.reward_action, name='reward_action'),
    path('options/<int:submanager_id>', views.sub_manager_option, name='sub_manager_options'),
    path('history/<int:submanager_id>', views.history, name='history')
]
