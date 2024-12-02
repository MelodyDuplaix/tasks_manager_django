from django.contrib import admin # type: ignore
from tasks.models import SubManager, TaskType, Task, Reward, Action, PonctualTask

class TaskTypeAdmin(admin.ModelAdmin):
  list_display = ("name", "sub_manager",)

class TaskAdmin(admin.ModelAdmin):
  list_display = ("name", "coins_number", "type",)

class RewardAdmin(admin.ModelAdmin):
  list_display = ("name", "coins_number", "sub_manager",)

class ActionAdmin(admin.ModelAdmin):
  list_display = ("name", "date","type","coins_number","sub_manager",)

class SubManagerAdmin(admin.ModelAdmin):
  list_display = ("name", "daily_objectif", "weekly_objectif", "monthly_objectif",)

class PonctualTaskAdmin(admin.ModelAdmin):
  list_display = ("name", "coins_number", "sub_manager",)

admin.site.register(SubManager, SubManagerAdmin)
admin.site.register(TaskType, TaskTypeAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(PonctualTask, PonctualTaskAdmin)
