# Diary Backend API

Backend для приложения-ежедневника на FastAPI и PostgreSQL с полным CRUD функционалом.

## 🚀 Возможности

- ✅ Создание записей
- ✅ Чтение записей (всех, по ID, поиск)
- ✅ Обновление записей
- ✅ Удаление записей
- ✅ Отметка записей как выполненных
- ✅ Фильтрация по статусу выполнения
- ✅ Валидация данных
- ✅ Автоматические временные метки

## 🛠️ Технологии

- **Python 3.12**
- **FastAPI** - современный async web framework
- **PostgreSQL** - реляционная база данных
- **SQLAlchemy 2.0** - async ORM
- **Docker** - контейнеризация
- **Pydantic** - валидация данных

## 📦 Установка и запуск

### 1. Клонирование репозитория
```
bash
git clone <your-repo-url>
cd diary-backend
```

### 2. Настройка окружения
```
Отредактируйте .env с вашими настройками:

POSTGRES_DB=diary_db
POSTGRES_USER=diary_user
POSTGRES_PASSWORD=diary_password
```

### 3. Запуск с Docker Compose
```
# Сборка и запуск контейнеров
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d

# Остановка контейнеров
docker-compose down
```

### 4. Доступ к приложению
```
После запуска приложение будет доступно по адресу:

- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
```

## 📡 API Endpoints

### 🔍 Получение записей
- **GET /api/v1/entries/** - Получить все записи
- **GET /api/v1/entries/{entry_id}** - Получить запись по ID
- **GET /api/v1/entries/search/{query}** - Поиск записей по заголовку

### ➕ Создание записи
- **POST /api/v1/entries/** - Создать новую запись

### ✏️ Обновление записи
- **PUT /api/v1/entries/{entry_id}** - Полное обновление записи
- **PATCH /api/v1/entries/{entry_id}/complete** - Изменить статус выполнения

### 🗑️ Удаление записи
- **DELETE /api/v1/entries/{entry_id}** - Удалить запись

### 🩺 Health Check
- **GET /health** - Проверка статуса приложения