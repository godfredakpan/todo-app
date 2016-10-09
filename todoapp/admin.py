from django.contrib import admin

from .models import ToDoList, Label


admin.site.register([ToDoList, Label])
