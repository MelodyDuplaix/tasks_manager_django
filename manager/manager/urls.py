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
from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.options, name='home'),
    path('add_submanager/', views.add_submanager, name='add_submanager'),
    path('delete_submanager/<int:submanager_id>', views.delete_submanager, name='delete_submanager'),
    path('<int:submanager_id>/', views.submanager_page, name='submanager_page'),
    path('action/<int:task_id>', views.task_action, name='task_action'),
    path('reward/<int:reward_id>', views.reward_action, name='reward_action'),
    path('options/<int:submanager_id>', views.sub_manager_option, name='sub_manager_options'),
    path('history/<int:submanager_id>', views.history, name='history'),
    path('<int:submanager_id>/add-task', views.add_task, name='add_task'),
    path('<int:submanager_id>/add-reward', views.add_reward, name='add_reward'),
    path('<int:submanager_id>/update-task/<int:task_id>', views.update_task, name='update_task'),
    path('<int:submanager_id>/update-reward/<int:reward_id>', views.update_reward, name='update_reward'),
    path('<int:submanager_id>/delete-task/<int:task_id>', views.delete_task, name='delete_task'),
    path('<int:submanager_id>/delete-reward/<int:reward_id>', views.delete_reward, name='delete_reward'),
    path('<int:submanager_id>/confirm-delete-task/<int:task_id>', views.confirm_delete_task, name='confirm_delete_task'),
    path('<int:submanager_id>/confirm-delete-reward/<int:reward_id>', views.confirm_delete_reward, name='confirm_delete_reward'),
    path('weekly/', views.weekly, name='weekly'),
    path('monthly/', views.monthly, name='monthly'),
    path('<int:submanager_id>/add-type', views.add_type, name='add_type'),
    path('<int:submanager_id>/delete-type/<int:type_id>', views.delete_type, name='delete_type'),
    path('<int:submanager_id>/update-type/<int:type_id>', views.update_type, name='update_type'),
    path('<int:submanager_id>/confirm-delete-type/<int:type_id>', views.confirm_delete_type, name='confirm_delete_type'),
]
