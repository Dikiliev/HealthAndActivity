from django.contrib import admin
from .models import User, Course, Lesson, Comment

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Comment)
