from django.urls import path
from django.contrib.auth import views as auth_views
from tasks.views.auth_views import profile, signup, password_reset, ResetPasswordView

urlpatterns = [
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'),
         name='password_change'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset_password/', ResetPasswordView.as_view(), name='password_reset'),
]
