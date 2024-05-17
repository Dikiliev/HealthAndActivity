# Dockerfile

# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Экспонируем порт
EXPOSE 8000

# Запускаем приложение
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "congig.wsgi:application"]
