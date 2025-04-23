from django.urls import path, include

app_name = 'tasks'
urlpatterns = [
    path('', include('tasks.urls.views')),
    path('accounts/', include('tasks.urls.accounts')),
    path('submanager/', include('tasks.urls.submanager')),
    path('tasks/', include('tasks.urls.tasks')),
    path('rewards/', include('tasks.urls.rewards')),
    path('statistics/', include('tasks.urls.statistics')),
    path('types/', include('tasks.urls.type')),
    path('ia/', include('tasks.urls.ia')),
]
