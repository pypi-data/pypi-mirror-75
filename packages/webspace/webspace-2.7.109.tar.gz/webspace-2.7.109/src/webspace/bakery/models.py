from django.db import models


class TaskBuild(models.Model):
    date_start = models.DateTimeField(null=True, blank=True, auto_now=True)
    date_end = models.DateTimeField(null=True, blank=True)
    task_id = models.CharField(max_length=100, default=None, null=True, blank=True)
    ready = models.BooleanField(default=False)

    def __str__(self):
        return str(self.task_id)

    class Meta:
        ordering = ['-date_start']
