from django.urls import path
from tasks.views.type_views import add_type, delete_type, update_type, confirm_delete_type

urlpatterns = [
    path('<int:submanager_id>/add-type/', add_type, name='add_type'),
    path('<int:submanager_id>/delete-type/<int:type_id>/', delete_type, name='delete_type'),
    path('<int:submanager_id>/update-type/<int:type_id>/', update_type, name='update_type'),
    path('<int:submanager_id>/confirm-delete-type/<int:type_id>/', confirm_delete_type,
         name='confirm_delete_type'),
]
