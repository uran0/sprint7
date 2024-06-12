from django.contrib import admin
from .models import Status, Tag, Priority, Task

# Register your models here.
admin.site.register(Status)
admin.site.register(Tag)
admin.site.register(Priority)

@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    list_filter= ["user"]