from django.urls import path
from tasks.views.task_views import add_task, delete_ponctual_task, delete_task, task_action, update_task, confirm_delete_ponctual_task, confirm_delete_task, add_ponctual_task, ponctual_task_action, update_ponctual_task, delete_ponctual_task

urlpatterns = [
    path('action/<int:task_id>/', task_action, name='task_action'),
    path('<int:submanager_id>/add-task/', add_task, name='add_task'),
    path('<int:submanager_id>/update-task/<int:task_id>/', update_task, name='update_task'),
    path('<int:submanager_id>/delete-task/<int:task_id>/', delete_task, name='delete_task'),
    path('<int:submanager_id>/confirm-delete-task/<int:task_id>/', confirm_delete_task, name='confirm_delete_task'),
    path('<int:submanager_id>/add-ponctual-task/', add_ponctual_task, name='add_ponctual_task'),
    path('ponctual-action/<int:task_id>/', ponctual_task_action, name='ponctual_task_action'),
    path('<int:submanager_id>/update-ponctual-task/<int:task_id>/', update_ponctual_task,
         name='update_ponctual_task'),
    path('<int:submanager_id>/confirm-delete-ponctual-task/<int:task_id>/', confirm_delete_ponctual_task,
         name='confirm_delete_ponctual_task'),
    path('<int:submanager_id>/delete-ponctual-task/<int:task_id>/', delete_ponctual_task,
         name='delete_ponctual_task'),
    path('delete_ponctual_task/<int:task_id>/', delete_ponctual_task,
         name='delete_ponctual_task'),
]
