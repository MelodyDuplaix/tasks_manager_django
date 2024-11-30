from django.contrib import admin
from tasks.models import SubManager, TaskType, task, Reward, Action, Objectif

admin.site.register(SubManager)
admin.site.register(TaskType)
admin.site.register(task)
admin.site.register(Reward)
admin.site.register(Action)
admin.site.register(Objectif)
