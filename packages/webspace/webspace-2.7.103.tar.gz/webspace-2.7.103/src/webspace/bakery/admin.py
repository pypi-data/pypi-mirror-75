from django.contrib import admin

from .models import TaskBuild


class TaskBuildAdmin(admin.ModelAdmin):
    search_fields = ('task_id',)
    list_display = ('task_id', 'ready', 'date_start', 'date_end')


admin.site.register(TaskBuild, TaskBuildAdmin)
