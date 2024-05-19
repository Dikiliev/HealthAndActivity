from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username

    def exist(self):
        return len(User.objects.filter(username=self.username)) > 0


class Course(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]

    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    author = models.CharField(max_length=150, blank=True, verbose_name='Автор')
    avatar = models.ImageField(blank=True, verbose_name='Аватарка')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )

    def __str__(self):
        return f'{self.title} ({self.author})'

    def get_short_description(self):
        max_len = 80

        if len(str(self.description)) <= max_len:
            return self.description

        return self.description[:max_len - 3] + '...'

    def get_lessons_count(self):
        return len(self.lessons.all())


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='урок', related_name='lessons')

    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(blank=True, verbose_name='Картина')

    def __str__(self):
        return f'{self.title} ({self.course.title})'

    def get_image_url(self):
        return self.image.url

    def get_short_title(self):
        max_len = 100

        if len(str(self.title)) <= max_len:
            return self.title

        return self.title[:max_len - 3] + '...'
