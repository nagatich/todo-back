from django.contrib import admin

from .models import *

admin.site.register(TodoList)
admin.site.register(TodoItem)
