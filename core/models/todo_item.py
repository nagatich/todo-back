from django.db import models
from django.contrib.auth.models import User

PRIORITY_CHOICES = (
    (0, 'Low'),
    (1, 'Medium'),
    (2, 'High'),
)

class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=500, verbose_name='Название')
    task = models.TextField(verbose_name='Задача')
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1, verbose_name='Приоритет')
    is_private = models.BooleanField(default=True, verbose_name='Приватная задача')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.user.username}: {self.name}'

    @property
    def parents(self):
        parents = self.todolist_set.filter(tasks__id=self.id)
        return [parent.id for parent in parents]
