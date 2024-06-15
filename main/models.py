from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg


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
    avatar = models.ImageField(blank=True, verbose_name='Аватарка')
    image = models.ImageField(blank=True, verbose_name='Картинка')
    description = models.TextField(blank=True, verbose_name='Описание')
    author = models.CharField(max_length=150, blank=True, verbose_name='Автор')

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )

    def __str__(self):
        return f'{self.title} ({self.author})'

    def get_image_url(self):
        if self.image:
            return self.image.url

        return False

    def get_short_description(self):
        max_len = 80

        if len(str(self.description)) <= max_len:
            return self.description

        return self.description[:max_len - 3] + '...'


    def get_average_rating(self):
        average_rating = self.comments.aggregate(Avg('rating'))['rating__avg']
        if average_rating:
            return round(average_rating, 1)

        return 0

    def get_comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='comments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='comments')
    text = models.TextField(verbose_name='Текст комментария')
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'Комментарий {self.text} от {self.author.username} к курсу {self.course.title}'
