from django.contrib import admin
from tasks.models import SubManager, TaskType, Task, Reward, Action

class TaskTypeAdmin(admin.ModelAdmin):
  list_display = ("name", "sub_manager",)

class TaskAdmin(admin.ModelAdmin):
  list_display = ("name", "coins_number","ponctuel", "type",)

class RewardAdmin(admin.ModelAdmin):
  list_display = ("name", "coins_number", "sub_manager",)

class ActionAdmin(admin.ModelAdmin):
  list_display = ("name", "date","type","coins_number","sub_manager",)

class SubManagerAdmin(admin.ModelAdmin):
  list_display = ("name", "daily_objectif", "weekly_objectif", "monthly_objectif",)


admin.site.register(SubManager, SubManagerAdmin)
admin.site.register(TaskType, TaskTypeAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(Action, ActionAdmin)
