from django.contrib import admin

from todo.models import Task, Comments, Image, TaskStatus

# Register your models here.
admin.site.register(TaskStatus)
admin.site.register(Task)
admin.site.register(Comments)
admin.site.register(Image)
