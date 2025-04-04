from django.urls import path
from tasks.views.statistics_views import history, weekly, monthly, yearly, statistics

urlpatterns = [
    path('history/<int:submanager_id>/', history, name='history'),
    path('weekly/', weekly, name='weekly'),
    path('monthly/', monthly, name='monthly'),
    path('yearly/', yearly, name='yearly'),
    path('<int:submanager_id>/statistics/', statistics, name='statistics'),
]
