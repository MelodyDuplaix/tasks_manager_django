from django.urls import path
from tasks.views.objectif_views import create_objective, save_tasks

urlpatterns = [
    path('create_objective/<int:submanager_id>/', create_objective, name='create_objective'),
    path('save_tasks/<int:submanager_id>/', save_tasks, name='save_tasks'),
]
