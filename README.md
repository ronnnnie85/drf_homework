# 📘 Django LMS API — обновлённый README

Ниже — доработанная версия README для проекта на **Django + Django REST Framework** (модуль LMS и платежи). Добавлены: чёткий quickstart, таблица переменных окружения, раздел про пагинацию/сортировку/фильтрацию с примерами, curl‑примеры, раздел «Тестирование», а также навигация по кастомным management‑командам.

---

## 🔎 Оглавление
- [Требования](#-требования)
- [Быстрый старт](#-быстрый-старт)
- [Переменные окружения](#-переменные-окружения)
- [Запуск и доступ](#-запуск-и-доступ)
- [API](#-api)
  - [LMS (`/lms/`)](#lms-lms)
  - [Пользователи и платежи (`/users/`)](#-пользователи-и-платежи-users)
  - [Параметры запроса: фильтры, сортировка, пагинация](#-параметры-запроса-фильтры-сортировка-пагинация)
  - [Примеры запросов](#-примеры-запросов)
- [Кастомные management‑команды](#-кастомные-management-команды)
- [Структура проекта](#-структура-проекта)
- [Тестирование](#-тестирование)
- [Полезное](#-полезное)

---

## ✅ Требования
- Python 3.11+
- pip, venv
- SQLite (по умолчанию) или другая БД, настроенная в `settings.py`

## 🚀 Быстрый старт
```bash
# 1) Клонирование
git clone <repo_url>
cd <project_name>

# 2) Виртуальное окружение и зависимости
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3) Конфигурация окружения
cp .env_sample .env
# отредактируйте значения под себя

# 4) Миграции и базовые данные
python manage.py migrate
python manage.py csu                 # создаст суперпользователя из .env
python manage.py seed_courses_lessons
python manage.py create_payments

# 5) Запуск dev‑сервера
python manage.py runserver
```

## 🔐 Переменные окружения
| Ключ          | Пример                | Описание                            |
|---------------|-----------------------|-------------------------------------|
| `ADMIN_MAIL`  | `admin@example.com`   | Логин суперпользователя для `csu`   |
| `ADMIN_PASS`  | `supersecret`         | Пароль суперпользователя для `csu`  |
| `DEBUG`       | `True`                | Режим отладки                       |
| `SECRET_KEY`  | `your_secret_key`     | Секретный ключ Django               |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | Разрешённые хосты                  |

> ⚠️ Никогда не коммитьте `.env` — добавьте его в `.gitignore`.

## 🌐 Запуск и доступ
- Админка: <http://127.0.0.1:8000/admin/>
- LMS API: <http://127.0.0.1:8000/lms/>
- Пользователи/платежи: <http://127.0.0.1:8000/users/>

## 🧩 API

### LMS (`/lms/`)
| Метод | URL                     | Описание                   |
|------:|-------------------------|----------------------------|
| GET   | `/lms/courses/`         | Список курсов              |
| GET   | `/lms/courses/<id>/`    | Курс с уроками             |
| POST  | `/lms/courses/`         | Создать курс               |
| PUT/PATCH | `/lms/courses/<id>/`| Обновить курс              |
| DELETE | `/lms/courses/<id>/`   | Удалить курс               |
| GET   | `/lms/lessons/`         | Список всех уроков         |
| POST  | `/lms/lessons/create/`  | Создать урок               |
| GET   | `/lms/lessons/<id>/`    | Просмотр урока             |
| PUT/PATCH | `/lms/lessons/<id>/update/` | Обновление урока |
| DELETE | `/lms/lessons/<id>/delete/`   | Удаление урока   |

### 👥 Пользователи и платежи (`/users/`)
| Метод | URL                         | Описание                |
|------:|-----------------------------|-------------------------|
| GET   | `/users/payments/`          | Получить все оплаты     |
| POST  | `/users/payments/`          | Добавить оплату         |
| GET   | `/users/payments/<id>/`     | Получить оплату         |
| PUT/PATCH | `/users/payments/<id>/` | Изменить оплату         |
| DELETE | `/users/payments/<id>/`    | Удалить оплату          |

#### 🔧 Параметры запроса: фильтры, сортировка, пагинация
- **Фильтры**: `?paid_course=<id>&payment_method=<cash|card|transfer>`
- **Сортировка**: `?ordering=payment_date` (добавьте `-` для убывания: `?ordering=-payment_date`)
- **Пагинация** (стандарт DRF):
  - `?page=2` — номер страницы
  - `?page_size=20` — размер страницы (если разрешено настройками)

#### 📎 Примеры запросов
```bash
# Список курсов
curl -s http://127.0.0.1:8000/lms/courses/

# Курс по id
curl -s http://127.0.0.1:8000/lms/courses/1/

# Создать курс (пример)
curl -s -X POST http://127.0.0.1:8000/lms/courses/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Математика"}'

# Платежи с фильтрами и сортировкой
curl -s "http://127.0.0.1:8000/users/payments/?paid_course=1&payment_method=cash&ordering=-payment_date"

# Пагинация платежей
curl -s "http://127.0.0.1:8000/users/payments/?page=2&page_size=20"
```

> ℹ️ Аутентификация: если включите пермишены/аутентификацию в DRF (например, TokenAuth), добавьте сюда раздел с требуемыми заголовками.

## ⚙️ Кастомные management‑команды
- `seed_courses_lessons` — создаёт тестовые курсы и уроки, предварительно очищая таблицы.
- `create_payments` — добавляет 3 тестовых оплаты (2 за уроки, 1 за курс).
- `csu` — создаёт суперпользователя из переменных `.env` (`ADMIN_MAIL`, `ADMIN_PASS`).

Примеры:
```bash
python manage.py seed_courses_lessons
python manage.py create_payments
python manage.py csu
```

## 🧱 Структура проекта
```
config/
 ├── urls.py                # Главный роутинг проекта
lms/
 ├── models.py              # Course, Lesson
 ├── serializers.py         # DRF‑сериализаторы
 ├── views.py               # CourseViewSet, Lesson CRUD
 ├── urls.py                # Роутинг /lms/
 ├── management/commands/
 │    ├── seed_courses_lessons.py
 │    ├── create_payments.py
 │    └── csu.py
users/
 ├── models.py              # User, Payment
 ├── views.py               # PaymentViewSet
 ├── urls.py                # Роутинг /users/
.env_sample                 # пример конфигурации окружения
```

## 🧪 Тестирование
```bash
# Запуск всех тестов
pytest -q

# С пояснениями/покрытием (если настроено)
pytest -q -vv --cov
```

## 🧰 Полезное
- Проверьте `settings.py` на предмет включённой пагинации DRF (`REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS']`, `PAGE_SIZE`).
- Добавьте Docker/Compose при необходимости — тогда здесь появится раздел «Запуск через Docker».
- Откройте Issue/PR шаблоны для более формального процесса разработки.

