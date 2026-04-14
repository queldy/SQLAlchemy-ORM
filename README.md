# Course Platform — SQLAlchemy ORM Backend

Онлайн-платформа для курсов (аналог Coursera/Udemy), реализованная с использованием **SQLAlchemy ORM** и **SQLite**.

---

## Домен

Платформа для онлайн-обучения, где:
- **Инструкторы** создают и ведут курсы
- **Студенты** записываются на курсы и отслеживают прогресс
- **Теги** помогают категоризировать курсы

---

## Модели

| Модель | Описание |
|---|---|
| `User` | Пользователь (инструктор или студент) |
| `UserProfile` | Профиль пользователя (1:1 с User) |
| `Course` | Курс, привязан к инструктору |
| `Tag` | Тег для категоризации курсов |
| `Enrollment` | Запись студента на курс (с прогрессом) |

---

## Связи между таблицами

### 1:1 — User ↔ UserProfile
Каждый пользователь имеет ровно один профиль с именем, bio, страной и сайтом.

```python
profile = relationship("UserProfile", back_populates="user", uselist=False)
```

### 1:N — User (instructor) → Course
Один инструктор может создать много курсов.

```python
courses_taught = relationship("Course", back_populates="instructor")
```

### N:N — Course ↔ Tag (через `course_tags`)
Курс может иметь несколько тегов; тег — на нескольких курсах.

```python
tags = relationship("Tag", secondary=course_tags, back_populates="courses")
```

### N:N с данными — User (student) ↔ Course (через `Enrollment`)
Студент записывается на курс. `Enrollment` хранит дополнительные поля: `enrolled_at`, `progress`.

```python
enrollments = relationship("Enrollment", back_populates="student")
```

---

## Структура проекта

```
course_platform/
├── main.py                    #  Точка входа — демонстрация всего
├── seed_data.py               #  Заполнение БД реалистичными данными
├── requirements.txt
│
├── db/
│   ├── __init__.py
│   └── database.py            # Engine, Session, Base, init_db()
│
├── models/
│   ├── __init__.py
│   ├── user.py                # User, UserProfile
│   ├── course.py              # Course, Tag, course_tags
│   └── enrollment.py          # Enrollment
│
├── crud/
│   ├── __init__.py
│   ├── user_crud.py           # CRUD + get_or_create для User
│   ├── course_crud.py         # CRUD для Course и Tag
│   └── enrollment_crud.py     # CRUD для Enrollment
│
└── queries/
    ├── __init__.py
    └── advanced_queries.py    # JOIN, фильтрация, агрегация
```

---

## Как запустить

### 1. Установить зависимости

```bash
pip install -r requirements.txt
```

### 2. Запустить полную демонстрацию

```bash
cd course_platform
python main.py
```

Скрипт автоматически:
- создаёт БД (`course_platform.db`)
- заполняет тестовыми данными
- выполняет все CRUD операции
- выполняет все запросы с выводом

---

## Реализованные требования

### Part 1 — Моделирование данных
-  **1:1** — `User` ↔ `UserProfile`
-  **1:N** — `User` (инструктор) → `Course`
-  **N:N** — `Course` ↔ `Tag` через таблицу `course_tags`
-  **N:N с данными** — `User` (студент) ↔ `Course` через `Enrollment`

### Part 2 — CRUD
-  **Create** — `create_user`, `create_course`, `enroll_student`
-  **Read** — поиск по ID, email, username, title
-  **Update** — обновление email, прогресса, профиля
-  **Delete** — удаление пользователя (cascade), курса, записи

### Part 3 — Запросы
-  Поиск по ID
-  Поиск по полю (email, username, title через ILIKE)
-  Получение связанных данных (все курсы инструктора, все студенты курса)
-  Фильтрация через связь (курсы по тегу, пользователи по стране)

### Part 4 — Данные
-  4 пользователя с профилями
-  4 курса с тегами
-  6 записей о зачислении с прогрессом

### Part 5 — Демонстрация
-  `main.py` — единый скрипт для запуска всего

###  Бонусы
-  `get_or_create` для User и Tag
-  Уникальные ограничения: `email`, `username`, `tag.name`, `(student_id, course_id)`
-  Валидация данных через `@validates` (email формат, price >= 0, progress 0–100)
-  Логирование SQL-запросов (SQLAlchemy `echo`)
-  Сложные JOIN-запросы с агрегацией (`GROUP BY`, `AVG`, `COUNT`)
-  `CASCADE` при удалении (профиль удаляется вместе с пользователем)
