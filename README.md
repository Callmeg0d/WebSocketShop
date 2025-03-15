# Веб-приложение с технологией WebSockets  

## Используемый стек технологий  

### Backend  
- **Python** – основной язык программирования  
- **FastAPI** – фреймворк для создания API  
- **Pydantic** – валидация данных и работа с моделями  
- **SQLAlchemy** – ORM для работы с базой данных  
- **Alembic** – инструмент управления миграциями БД  

### Базы данных и фоновые задачи  
- **PostgreSQL** – реляционная база данных для хранения основной информации  
- **Redis** – NoSQL-хранилище в роли брокера задач  
- **Celery** – обработка фоновых задач  

### DevOps и контейнеризация  
- **Docker** – контейнеризация приложения  
- **Docker Compose** – управление многоконтейнерными сервисами  

### Frontend  
- **HTML, CSS** – базовая разметка и стилизация  

### Тестирование  
- **Pytest** – тестирование кода

## Подключение через Docker
- docker-compose up -d --build
- Приложение будет доступно по адресу: http://localhost:7777
- Документация Swagger будет доступна по адресу: http://localhost:7777/docs
