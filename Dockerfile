# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем зависимости для Python и Django
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Выполняем миграции и собираем статику
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Открываем порт 8000 для приложения
EXPOSE 8000

# Запускаем приложение
CMD ["gunicorn", "HealthAndActivity.wsgi:application", "--bind", "0.0.0.0:8000"]
