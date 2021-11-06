from django.db import models
from django.contrib.auth.models import User

from .todo_item import TodoItem

PRIORITY_CHOICES = (
    (0, 'Low'),
    (1, 'Medium'),
    (2, 'High'),
)

class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=500, verbose_name='Название')
    tasks = models.ManyToManyField(to=TodoItem, verbose_name='Задачи', blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1, verbose_name='Приоритет')
    is_private = models.BooleanField(default=True, verbose_name='Приватный список')

    class Meta:
        verbose_name = 'Список задач'
        verbose_name_plural = 'Списки задач'

    def __str__(self):
        return f'{self.user.username}: {self.name}'

