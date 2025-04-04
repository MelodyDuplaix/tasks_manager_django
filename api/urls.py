from django.urls import path
from .views import login_view, password_reset_request, password_change

urlpatterns = [
    path('login/', login_view, name='login'),
    path('password/reset/', password_reset_request, name='password_reset_request'),
    path('password/change/', password_change, name='password_change'),
]
