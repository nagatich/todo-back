# Generated by Django 3.1.7 on 2021-10-13 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('task', models.TextField(verbose_name='Задача')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('priority', models.IntegerField(choices=[(0, 'Low'), (1, 'Medium'), (2, 'High')], default=1, verbose_name='Приоритет')),
                ('is_private', models.BooleanField(default=True, verbose_name='Приватная задача')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('priority', models.IntegerField(choices=[(0, 'Low'), (1, 'Medium'), (2, 'High')], default=1, verbose_name='Приоритет')),
                ('is_private', models.BooleanField(default=True, verbose_name='Приватный список')),
                ('tasks', models.ManyToManyField(to='core.TodoItem', verbose_name='Задачи')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Список задач',
                'verbose_name_plural': 'Списки задач',
            },
        ),
    ]
