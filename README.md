# Machine Monitoring System

##  Описание
Проект реализует:
1. **Периодический опрос эндпоинтов** 30 серверов каждые 15 минут.
2. **Мониторинг ресурсов** с детектированием аномалий:
   - CPU > 85% в течение 30 минут
   - Memory > 90% в течение 30 минут
   - Disk > 95% в течение 2 часов
3. Запись данных и инцидентов в БД.

## Запуск проекта
### Сборка и запуск контейнеров
```bash
docker-compose up --build -d
```

## Переменные окружения
```env
MYSQL_DATABASE=monitoring
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_ROOT_PASSWORD=root_password
```

## API
- **Получение активных инцидентов:**
  ```bash
  curl http://localhost:8000/api/incidents/
  ```
