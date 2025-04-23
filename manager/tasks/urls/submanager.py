from django.urls import path
from tasks.views.submanager_views import add_submanager, delete_submanager, activate_submanager, desactivate_submanager, submanager_page

urlpatterns = [
    path('add_submanager/', add_submanager, name='add_submanager'),
    path('delete_submanager/<int:submanager_id>/', delete_submanager, name='delete_submanager'),
    path('<int:submanager_id>/', submanager_page, name='submanager_page'),
    path('activate_submanager/<int:submanager_id>/', activate_submanager, name='activate_submanager'),
    path('desactivate_submanager/<int:submanager_id>/', desactivate_submanager, name='desactivate_submanager'),
    path('<int:submanager_id>/detail/', submanager_page, name='submanager_detail'),
]
