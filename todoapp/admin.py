from django.contrib import admin

from .models import TodoList, Label


admin.site.register([TodoList, Label])
