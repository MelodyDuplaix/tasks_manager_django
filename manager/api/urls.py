from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import password_reset_request, password_change, get_user_submanagers, get_user_id

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('password/reset/', password_reset_request, name='password_reset_request'),
    path('password/change/', password_change, name='password_change'),
    path('submanagers/', get_user_submanagers, name='get_user_submanagers'),
    path('user/id/', get_user_id, name='get_user_id'),
]
