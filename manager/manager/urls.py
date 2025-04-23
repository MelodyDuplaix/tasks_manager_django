"""
URL configuration for manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # type: ignore
from django.urls import path, include  # type: ignore
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('password_change/', include('tasks.urls.accounts'), name='password_change'),
    path('accounts/', include('tasks.urls.accounts'), name='accounts'),
    path('', include('tasks.urls.views'), name='home'),
    path('submanager/', include('tasks.urls.submanager'), name='submanager'),
    path('tasks/', include('tasks.urls.tasks'), name='tasks'),
    path('rewards/', include('tasks.urls.rewards'), name='rewards'),
    path('statistics/', include('tasks.urls.statistics'), name='statistics'),
    path('types/', include('tasks.urls.type'), name='types'),
    path('api/', include('api.urls')),
    path('ia/', include('tasks.urls.ia')),
]

schema_view = get_schema_view(
   openapi.Info(
      title="Task Manager API",
      default_version='v1',
      description="""This API provides a comprehensive set of endpoints for managing tasks and rewards within a task management system. Key features include:

* **Authentication:** Secure access using JSON Web Tokens (JWT).
* **Task Management:** Create, read, update, and delete both recurring and punctual tasks. Tasks are associated with specific sub-managers and task types.
* **Reward Management:** Create, read, update, and delete rewards. Rewards are associated with sub-managers and have a defined coin value.
* **Reward Validation:** Validate rewards, deducting the reward's coin value from the sub-manager's total earned coins.
* **Action Tracking:** Tracks actions performed by sub-managers, including completing tasks and claiming rewards. Actions record the task type, coin value, and associated sub-manager.
* **Statistics:** Retrieve daily and total coin counts for individual sub-managers and the entire system.

The API is designed for efficient management of tasks and rewards, providing a clear and structured way to track progress and incentivize performance.  All endpoints require JWT authentication.""",
      contact=openapi.Contact(email="melo.surseine@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
