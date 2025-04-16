from django.urls import path
from .views import get_total_points_submanager, validate_reward, get_daily_total_points, get_total_points, mark_task_done, password_reset_request, password_change, get_user_submanagers, get_user_id, get_submanager_data
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('password/reset/', password_reset_request, name='password_reset_request'),
    path('password/change/', password_change, name='password_change'),
    path('submanagers/', get_user_submanagers, name='get_user_submanagers'),
    path('user/id/', get_user_id, name='get_user_id'),
    path('user/daily_coins/', get_daily_total_points, name='get_daily_total_points'),
    path('user/total_coins/', get_total_points, name='get_total_points'),
    path('user/total_coins/<int:submanager_id>/', get_total_points_submanager, name='get_total_points_submanager'),
    path('submanager/<int:submanager_id>/data/', get_submanager_data, name='get_submanager_data'),
    path('task/done/<int:task_id>/', mark_task_done, name='mark_task_done'),
    path('reward/validate/<int:reward_id>/', validate_reward, name='validate_reward'),
]
