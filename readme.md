# Falconix MVP Inference Service

Это MVP инференс-сервис проекта Falconix, представляющий API для поиска и ранжирования Telegram каналов.

## Описание

Сервис обрабатывает текст объявления и критерии фильтрации, чтобы найти и релевантые Telegram каналы для размещения рекламы.

## Быстрый старт

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/falconnix-inference-service.git
   ```

2. Соберите Docker образ:
   ```bash
   docker build -t falconnix-inference-service .
   ```

3. Запустите Docker контейнер:
   ```bash
   docker run -d -p 8000:8000 falconnix-inference-service
   ```

## Использование

### Эндпоинт: Поиск каналов

- **URL:** `/get_channels/`
- **Метод:** `POST`
- **Тело запроса:** JSON с минимальными критериями поиска
- **Ответ:** Список подходящих Telegram каналов.

---

