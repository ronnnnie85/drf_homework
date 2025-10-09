# 📘 Django LMS API

REST API для управления курсами, уроками и оплатами.  
Реализовано на **Django + Django REST Framework**, поддерживает фильтрацию, сортировку и имеет несколько кастомных management-команд.

---

## 🚀 Запуск проекта

### 1. Установка
```bash
git clone <repo_url>
cd <project_name>
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

---

### 2. Настройка окружения
В репозитории есть пример `.env_sample` — скопируй и переименуй его:
```bash
cp .env_sample .env
```
Заполни свои значения:
```env
ADMIN_MAIL=admin@example.com
ADMIN_PASS=supersecret
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=127.0.0.1,localhost
```

> ⚠️ `.env` не должен попадать в git — добавь его в `.gitignore`.

---

### 3. Миграции и создание суперпользователя
```bash
python manage.py migrate
python manage.py csu
```
Команда `csu` создаст суперпользователя, используя данные из `.env`.

---

### 4. Запуск сервера
```bash
python manage.py runserver
```
После запуска:
- Админ-панель → [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- API → [http://127.0.0.1:8000/lms/](http://127.0.0.1:8000/lms/)
- Пользователи/платежи → [http://127.0.0.1:8000/users/](http://127.0.0.1:8000/users/)

---

## 🧩 Основные эндпоинты API

### 📚 LMS-модуль (`/lms/`)
| Метод | URL | Описание |
|--------|-----|-----------|
| `GET` | `/lms/courses/` | Получить список курсов |
| `GET` | `/lms/courses/<id>/` | Получить курс с уроками |
| `POST` | `/lms/courses/` | Создать курс |
| `PUT/PATCH` | `/lms/courses/<id>/` | Обновить курс |
| `DELETE` | `/lms/courses/<id>/` | Удалить курс |
| `GET` | `/lms/lessons/` | Список всех уроков |
| `POST` | `/lms/lessons/create/` | Создание урока |
| `GET` | `/lms/lessons/<id>/` | Просмотр урока |
| `PUT/PATCH` | `/lms/lessons/<id>/update/` | Обновление урока |
| `DELETE` | `/lms/lessons/<id>/delete/` | Удаление урока |

---

### 💳 Пользователи и платежи (`/users/`)
| Метод | URL | Описание |
|--------|-----|-----------|
| `GET` | `/users/payments/` | Получить все оплаты |
| `POST` | `/users/payments/` | Добавить оплату |
| `GET` | `/users/payments/<id>/` | Получить оплату |
| `PUT/PATCH` | `/users/payments/<id>/` | Изменить оплату |
| `DELETE` | `/users/payments/<id>/` | Удалить оплату |
| 🔍 Фильтры | `?paid_course=1&payment_method=cash` |
| ↕️ Сортировка | `?ordering=payment_date` |

---

## ⚙️ Кастомные management-команды

### 🧮 `seed_courses_lessons`
Создает 2 тестовых курса (*Математика*, *Физика*) и по 2 урока на каждый.  
Очищает таблицы `Course` и `Lesson` перед добавлением.
```bash
python manage.py seed_courses_lessons
```
**Вывод:**
```
Удалено: уроков=4, курсов=2
Создано: курсов=2, уроков=4
```

---

### 💳 `create_payments`
Добавляет 3 тестовых оплаты:
- 2 за уроки  
- 1 за курс  
(требуется наличие хотя бы одного пользователя и курсов).
```bash
python manage.py create_payments
```
**Вывод:**
```
🗑 Удалено старых записей: 3
Успешно добавлено 3 записи в таблицу Payment
```

---

### 👤 `csu`
Создает суперпользователя из данных `.env` (`ADMIN_MAIL`, `ADMIN_PASS`).
```bash
python manage.py csu
```
**Вывод:**
```
Superuser создан: admin@example.com
```

---

## 🧱 Структура проекта

```
config/
 ├── urls.py               # Главный роутинг проекта
lms/
 ├── models.py             # Course, Lesson
 ├── serializers.py        # DRF-сериализаторы
 ├── views.py              # CourseViewSet, Lesson CRUD
 ├── urls.py               # Роутинг /lms/
 ├── management/commands/
 │    ├── seed_courses_lessons.py
 │    ├── create_payments.py
 │    └── csu.py
users/
 ├── models.py             # User, Payment
 ├── views.py              # PaymentViewSet
 ├── urls.py               # Роутинг /users/
.env_sample                # пример конфигурации окружения
```
