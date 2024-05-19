import json
import random

from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect

from .models import User, Course, Lesson

DEFAULT_TITLE = 'EvaTutorials'


def home(request: HttpRequest):
    return redirect('catalog')


def catalog(request: HttpRequest):
    data = create_base_data('Каталог')
    data['courses'] = []

    courses = Course.objects.filter(status='accepted')
    data['courses'] = courses

    return render(request, 'catalog.html', data)


def about_us(request: HttpRequest):
    data = create_base_data('О нас')
    return render(request, 'about_us.html', data)


def show_lesson(request: HttpRequest, lesson_id: int):
    lesson = Lesson.objects.get(id=lesson_id)
    course = lesson.course

    lessons = course.lessons.all()
    index = list(lessons).index(lesson)

    data = create_base_data(f'Урок: {lesson.title}')
    data['lesson'] = lesson

    if index > 0:
        data['previous_lesson_id'] = lessons[index - 1].id

    if index < len(lessons) - 1:
        data['next_lesson_id'] = lessons[index + 1].id

    return render(request, 'lesson.html', data)


def show_course(request: HttpRequest, course_id: int):
    course = Course.objects.get(id=course_id)

    data = create_base_data(f'Курс: {course.title}')
    data['course'] = course
    data['lessons'] = course.lessons.all()

    print(data)
    return render(request, 'course.html', data)


def create_course(request: HttpRequest):
    data = create_base_data()

    def get():
        return render(request, 'create_course.html', data)

    def post():
        post_data = request.POST
        lessons = []

        course_title = post_data['course_title']
        course_description = post_data['course_description']
        course_image = request.FILES['course_image']
        course = Course(title=course_title, description=course_description, avatar=course_image, author=request.user)

        lesson_index = 1
        while True:
            lesson_title = post_data.get(f'lesson_title_{lesson_index}', '')
            lesson_description = post_data.get(f'lesson_description_{lesson_index}', '')

            lesson_image = request.FILES.get(f'lesson_image_{lesson_index}', None)

            if not all([lesson_title, lesson_description]):
                break

            lesson = Lesson(title=lesson_title, description=lesson_description, image=lesson_image)
            lessons.append(lesson)

            lesson_index += 1

        course.save()
        for lesson in lessons:
            lesson.course = course
            lesson.save()

        return redirect('thanks')

    if request.method == 'POST':
        return post()
    return get()


def thanks(request: HttpRequest):
    data = create_base_data()
    return render(request, 'thanks.html', data)


def register(request: HttpRequest):
    data = create_base_data('Регистрация')

    def get():
        return render(request, 'registration/register.html', data)

    def post():
        post_data = request.POST

        user = User()
        user.username = post_data.get('username', '')
        user.email = post_data.get('email', '')
        user.first_name = post_data.get('first_name', '')
        user.last_name = post_data.get('last_name', '')

        password = post_data.get('password', '')

        data['username'] = user.username
        data['email'] = user.email
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name

        def check_validate():
            if len(user.username) < 3:
                data['error'] = '* Имя пользователся должно состоять как минимум из 3 симьволов'
                return False

            if user.exist():
                data['error'] = '* Такой пользователь уже существует'
                return False

            if len(password) < 8:
                data['error'] = '* Пароль должен состоять как минимум из 8 симьволов'
                return False
            return True

        if not check_validate():
            return render(request, 'registration/register.html', data)

        user.set_password(password)
        user.save()
        login(request, user)

        return redirect('home')

    if request.method == 'POST':
        return post()
    return get()


def user_login(request: HttpRequest):
    data = create_base_data('Вход')

    def get():
        return render(request, 'registration/login.html')

    def post():
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            return redirect('home')

        data['error'] = '* Неверное имя пользователя или пароль'
        return render(request, 'registration/login.html', data)

    if request.method == 'POST':
        return post()
    return get()


def logout_user(request: HttpRequest):
    logout(request)
    return redirect('login')


# Help functions
def create_base_data(title: str = None):
    if not title:
        title = DEFAULT_TITLE

    return {
        'title': title,
    }
