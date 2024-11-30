from django.contrib import admin
from tasks.models import SubManager, TaskType, Task, Reward, Action, Objectif

class TaskTypeAdmin(admin.ModelAdmin):
  list_display = ("name", "sub_manager",)

class TaskAdmin(admin.ModelAdmin):
  list_display = ("name", "coins_number","ponctuel", "type",)

class RewardAdmin(admin.ModelAdmin):
  list_display = ("name", "coins_number", "sub_manager",)

class ActionAdmin(admin.ModelAdmin):
  list_display = ("name", "date","type","coins_number","sub_manager",)

class ObjectifAdmin(admin.ModelAdmin):
  list_display = ("name", "coins_number", "sub_manager",)

admin.site.register(SubManager)
admin.site.register(TaskType, TaskTypeAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Objectif, ObjectifAdmin)
