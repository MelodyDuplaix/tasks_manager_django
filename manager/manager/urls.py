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
from tasks.views import views  # type: ignore
from tasks.views.auth_views import profile, signup, password_reset, ResetPasswordView  # type: ignore
from tasks.views.submanager_views import add_submanager, delete_submanager, activate_submanager, desactivate_submanager, submanager_page   # type: ignore
from tasks.views.reward_views import add_reward, delete_reward, reward_action, update_reward, confirm_delete_reward  # type: ignore
from tasks.views.statistics_views import history, weekly, monthly, yearly, statistics  # type: ignore
from tasks.views.task_views import add_task, delete_ponctual_task, delete_task, task_action, update_task, confirm_delete_ponctual_task, confirm_delete_task, add_ponctual_task, ponctual_task_action, update_ponctual_task, delete_ponctual_task  # type: ignore
from tasks.views.type_views import add_type, delete_type, update_type, confirm_delete_type  # type: ignore
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'),
         name='password_change'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/signup/', signup, name='signup'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/reset_password/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('', views.options, name='home'),
    path('add_submanager/', add_submanager, name='add_submanager'),
    path('delete_submanager/<int:submanager_id>/', delete_submanager, name='delete_submanager'),
    path('<int:submanager_id>/', submanager_page, name='submanager_page'),
    path('action/<int:task_id>/', task_action, name='task_action'),
    path('reward/<int:reward_id>/', reward_action, name='reward_action'),
    path('options/<int:submanager_id>/', views.sub_manager_option, name='sub_manager_options'),
    path('history/<int:submanager_id>/', history, name='history'),
    path('<int:submanager_id>/add-task/', add_task, name='add_task'),
    path('<int:submanager_id>/add-reward/', add_reward, name='add_reward'),
    path('<int:submanager_id>/update-task/<int:task_id>/', update_task, name='update_task'),
    path('<int:submanager_id>/update-reward/<int:reward_id>/', update_reward, name='update_reward'),
    path('<int:submanager_id>/delete-task/<int:task_id>/', delete_task, name='delete_task'),
    path('<int:submanager_id>/delete-reward/<int:reward_id>/', delete_reward, name='delete_reward'),
    path('<int:submanager_id>/confirm-delete-task/<int:task_id>/', confirm_delete_task, name='confirm_delete_task'),
    path('<int:submanager_id>/confirm-delete-reward/<int:reward_id>/', confirm_delete_reward, name='confirm_delete_reward'),
    path('weekly/', weekly, name='weekly'),
    path('monthly/', monthly, name='monthly'),
    path('yearly/', yearly, name='yearly'),
    path('<int:submanager_id>/add-type/', add_type, name='add_type'),
    path('<int:submanager_id>/delete-type/<int:type_id>/', delete_type, name='delete_type'),
    path('<int:submanager_id>/update-type/<int:type_id>/', update_type, name='update_type'),
    path('<int:submanager_id>/confirm-delete-type/<int:type_id>/', confirm_delete_type,
         name='confirm_delete_type'),
    path('<int:submanager_id>/add-ponctual-task/', add_ponctual_task, name='add_ponctual_task'),
    path('ponctual-action/<int:task_id>/', ponctual_task_action, name='ponctual_task_action'),
    path('<int:submanager_id>/update-ponctual-task/<int:task_id>/', update_ponctual_task,
         name='update_ponctual_task'),
    path('<int:submanager_id>/confirm-delete-ponctual-task/<int:task_id>/', confirm_delete_ponctual_task,
         name='confirm_delete_ponctual_task'),
    path('<int:submanager_id>/delete-ponctual-task/<int:task_id>/', delete_ponctual_task,
         name='delete_ponctual_task'),
    path('activate_submanager/<int:submanager_id>/', activate_submanager, name='activate_submanager'),
    path('desactivate_submanager/<int:submanager_id>/', desactivate_submanager, name='desactivate_submanager'),
    path('<int:submanager_id>/delete-action/<int:action_id>/', views.delete_action, name='delete_action'),
    path('<int:submanager_id>/confirm-delete-action/<int:action_id>/', views.confirm_delete_action,
         name='confirm_delete_action'),
    path('<int:submanager_id>/statistics/', statistics, name='statistics'),
]
