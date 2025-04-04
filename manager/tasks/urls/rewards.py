from django.urls import path
from tasks.views.reward_views import add_reward, delete_reward, reward_action, update_reward, confirm_delete_reward

urlpatterns = [
    path('reward/<int:reward_id>/', reward_action, name='reward_action'),
    path('<int:submanager_id>/add-reward/', add_reward, name='add_reward'),
    path('<int:submanager_id>/update-reward/<int:reward_id>/', update_reward, name='update_reward'),
    path('<int:submanager_id>/delete-reward/<int:reward_id>/', delete_reward, name='delete_reward'),
    path('<int:submanager_id>/confirm-delete-reward/<int:reward_id>/', confirm_delete_reward, name='confirm_delete_reward'),
]
