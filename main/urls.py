from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('about-us/', views.about_us, name='about-us'),

    path('course/<int:course_id>/', views.show_course, name='course'),
    path('lesson/<int:lesson_id>/', views.show_lesson, name='lesson'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
