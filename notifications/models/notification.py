from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    message = models.CharField(max_length=512, verbose_name='Текст уведомления')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Для пользователя')
    seen = models.BooleanField(default=False, verbose_name='Прочитано')
    event = models.CharField(max_length=200, verbose_name='Событие', default='notification')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        
    def __str__(self):
        return f'{self.to_user.username} {self.message} {self.created}'
