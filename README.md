# DRF Homework -- Django REST API

Полноценный учебный REST API проект на **Django REST Framework** с
поддержкой:

-   PostgreSQL\
-   Redis\
-   Celery + Celery Beat\
-   Docker / Docker Compose\
-   CI/CD через GitHub Actions\
-   JWT-аутентификация\
-   Автоматическое развертывание на сервер

🌍 **Продакшен сервер:**\
http://158.160.190.68/

------------------------------------------------------------------------

# 📦 1. Функциональность проекта

-   Пользователи и авторизация через JWT\
-   Курсы, уроки, прогресс обучения\
-   Админ-панель Django\
-   Документация API (Swagger / ReDoc)\
-   Асинхронные задачи Celery\
-   Полная контейнеризация проекта

------------------------------------------------------------------------

# 🚀 2. Локальный запуск

## 2.1. Клонирование проекта

``` bash
git clone https://github.com/ronnnnie85/drf_homework.git
cd drf_homework
```

## 2.2. Установка виртуального окружения

``` bash
python -m venv venv
source venv/bin/activate        # Linux/MacOS
# .\venv\Scripts\activate    # Windows
```

## 2.3. Установка зависимостей

``` bash
pip install -r requirements.txt
```

## 2.4. Создание файла .env

``` bash
cp .env_sample .env
```

Отредактируйте переменные:

    DEBUG=True
    SECRET_KEY=yourkey
    POSTGRES_DB=drf_db
    POSTGRES_USER=drf_user
    POSTGRES_PASSWORD=password
    POSTGRES_HOST=localhost
    REDIS_HOST=localhost

## 2.5. Применение миграций и суперпользователь

``` bash
python manage.py migrate
python manage.py createsuperuser
```

## 2.6. Запуск сервера разработки

``` bash
python manage.py runserver
```

------------------------------------------------------------------------

# 🐳 3. Запуск через Docker / Docker Compose

## 3.1. Сборка образов

``` bash
docker compose build
```

## 3.2. Запуск контейнеров

``` bash
docker compose up -d
```

## 3.3. Остановка

``` bash
docker compose down
```

------------------------------------------------------------------------

# 🌐 4. Развертывание на сервере (VPS)

Проект развёрнут на сервере по адресу:\
**http://158.160.190.68/**

## 4.1. Установка Docker

``` bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin git
```

## 4.2. Подготовка директории проекта

``` bash
sudo mkdir -p /var/www/drf_homework
sudo chown -R $USER:$USER /var/www/drf_homework
cd /var/www/drf_homework
```

## 4.3. Клонирование репозитория

``` bash
git clone https://github.com/ronnnnie85/drf_homework.git .
```

## 4.4. Создание .env

``` bash
cp .env_sample .env
nano .env
```

## 4.5. Первый запуск на сервере

``` bash
docker compose up -d --build
```

------------------------------------------------------------------------

# 🔄 5. CI/CD (GitHub Actions)

При пуше в любую ветку:

1.  Запускаются тесты\
2.  Производится деплой на сервер в `/var/www/drf_homework`\


### Необходимые секреты GitHub:

  Название   Значение
  ---------- --------------------
  SSH_HOST   адрес
  SSH_USER   имя пользователя
  SSH_PORT   порт
  SSH_KEY    приватный SSH ключ

------------------------------------------------------------------------

# 📑 6. API Endpoints

Ниже представлена **структура API**, как в современной документации.

# 🔐 6.1. Аутентификация (JWT)

  Метод   URL                    Описание
  ------- ---------------------- ----------------------------------
  POST    `/api/auth/login/`     Получить access + refresh токены
  POST    `/api/auth/refresh/`   Обновить access-токен
  POST    `/api/auth/logout/`    Выйти (если реализовано)

### Пример ответа:

``` json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

------------------------------------------------------------------------

# 👤 6.2. Пользователи

  Метод   URL                     Описание
  ------- ----------------------- ----------------------------------------
  GET     `/api/users/profile/`   Получение данных текущего пользователя
  PUT     `/api/users/profile/`   Обновление профиля
  PATCH   `/api/users/profile/`   Частичное обновление

------------------------------------------------------------------------

# 🎓 6.3. Курсы

  Метод    URL
  -------- ---------------------------------------
  GET      `/api/courses/` -- список курсов
  POST     `/api/courses/` -- создать курс
  GET      `/api/courses/<id>/` -- получить курс
  PUT      `/api/courses/<id>/` -- обновить
  DELETE   `/api/courses/<id>/` -- удалить

------------------------------------------------------------------------

# 📘 6.4. Уроки

  Метод    URL
  -------- ----------------------
  GET      `/api/lessons/`
  POST     `/api/lessons/`
  GET      `/api/lessons/<id>/`
  PUT      `/api/lessons/<id>/`
  DELETE   `/api/lessons/<id>/`

------------------------------------------------------------------------

# 📈 6.5. Прогресс пользователя

  Метод   URL
  ------- --------------------------------------------------
  GET     `/api/progress/` -- получить прогресс
  POST    `/api/progress/` -- отметить урок как пройденный

------------------------------------------------------------------------

# 📄 6.6. Документация API

  Тип          URL
  ------------ ---------------
  Swagger UI   `/api/docs/`
  ReDoc        `/api/redoc/`

------------------------------------------------------------------------

# 🔧 7. Полезные команды

### Логи:

``` bash
docker compose logs -f
```

### Перезапуск:

``` bash
docker compose up -d --build
```

### Очистка контейнеров:

``` bash
docker system prune -a
```

