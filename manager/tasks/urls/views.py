from django.urls import path
from tasks.views import views

urlpatterns = [
    path('', views.options, name='home'),
    path('options/<int:submanager_id>/', views.sub_manager_option, name='sub_manager_options'),
    path('<int:submanager_id>/delete-action/<int:action_id>/', views.delete_action, name='delete_action'),
    path('<int:submanager_id>/confirm-delete-action/<int:action_id>/', views.confirm_delete_action,
         name='confirm_delete_action'),
]
