# Generated by Django 4.2.13 on 2024-05-19 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_lesson_video_src_lesson_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.CharField(choices=[('pending', 'На рассмотрении'), ('accepted', 'Принято'), ('rejected', 'Отклонено')], default='pending', max_length=10, verbose_name='Статус'),
        ),
    ]
