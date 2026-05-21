# План рефакторинга YTDL

Зафиксировано: 2026-05-21. Ветка работы: `dev`.

**Решения:**
- Транспорт между `bot` и `userbot` — **Redis** (очередь заданий, статусы, кэш `file_id`).
- Объём — полный (P0–P3): транспорт, сервисный слой, чистка, Docker, тесты.

## Проблема

Сейчас `bot` и `userbot` координируются пересылкой Python-словаря, сериализованного
в строку, через обычные Telegram-сообщения (`ast.literal_eval`). Последствия: нет
очереди и гарантии доставки, хрупкая адресация ответа через `message_id + 1`,
флаг `status` в SQLite как нерасторжимый мьютекс (не сбрасывается при падении userbot).

## Целевая архитектура

```
Пользователь ──ссылка──▶ bot/ (aiogram) ──▶ services
                                              │
                          LPUSH ytdl:tasks ──▶ Redis ──BRPOP──▶ userbot/ worker
                                              │  status (TTL)        │
                          слушает results ◀───┤  cache fileid        ▼
                                              └──────────────── youtube-dl
```

Telegram больше НЕ шина между процессами. Userbot всё ещё шлёт видеофайл боту через
Telegram (нужен `file_id`), но координация заданий и адресация ответов — через Redis.

## Этап 0 — Инфраструктура

| #   | Задача                                                                          | Файлы |
|-----|---------------------------------------------------------------------------------|-------|
| 0.1 | Добавить `redis` (asyncio-клиент) в requirements                                | `requirements.txt` |
| 0.2 | В `config.py`: `redis_host`, `redis_port`, `redis_db`, `redis_url`              | `config/config.py`, `.env_example` |
| 0.3 | Абсолютные пути от корня проекта (убрать `../`), корень через `Path(__file__)`  | `config/config.py`, `loader.py` |
| 0.4 | `docker-compose.yml`: сервисы `bot`, `userbot`, `redis`; volume для db/sessions | новый |
| 0.5 | `Dockerfile` (Python + ffmpeg), отдельные CMD для bot/userbot                   | новый |

**Проверка:** `docker-compose up redis` поднимается, конфиг читается из любого CWD.

## Этап 1 — Слой транспорта (P0, ядро)

| #   | Задача                                                                          | Файлы |
|-----|---------------------------------------------------------------------------------|-------|
| 1.1 | Создать пакет `utils/transport/`                                                | новый |
| 1.2 | `TaskQueue`: `push()`, `pop()` через `BRPOP`                                     | `utils/transport/queue.py` |
| 1.3 | `DownloadTask` — pydantic-модель (`url`, `user_id`, `chat_id`, `status_message_id`, `video_id`) | `utils/transport/models.py` |
| 1.4 | `ResultBus`: userbot публикует `DownloadResult` (file_id / ошибка), bot подписан | `utils/transport/result.py` |
| 1.5 | `StatusStore`: `set_busy/clear/is_busy` на ключах Redis с TTL (~10 мин)          | `utils/transport/status.py` |
| 1.6 | `FileCache`: `get/save` кэш `file_id` по `video_id`                              | `utils/transport/cache.py` |
| 1.7 | Зарегистрировать клиент Redis в `loader.py`                                      | `loader.py` |

Решения: адресацию ответа нести в задании явным `status_message_id` (конец
`message_id + 1`); TTL статуса = авто-разблокировка при падении; на этапе 1 кэш
пишем и в Redis, и в таблицу `links` — судьба таблицы решается на 4.2.

**Проверка:** юнит-тест round-trip — push/pop задания, сериализация модели.

## Этап 2 — Сервисный слой (P1)

| #   | Задача                                                                          | Файлы |
|-----|---------------------------------------------------------------------------------|-------|
| 2.1 | `bot/services/user_service.py` — регистрация, обновление, активность            | новый |
| 2.2 | `bot/services/download_service.py` — кэш → выдача / постановка в очередь, статус | новый |
| 2.3 | `handlers/user/video_url.py` — только парсинг апдейта + вызов сервиса            | существующий |
| 2.4 | `handlers/user/start.py` через `user_service`                                   | существующий |
| 2.5 | Удалить `handlers/host/text.py`, `handlers/host/video.py`; приём результата — listener | удаление + `bot/result_listener.py` |
| 2.6 | `result_listener` как фоновая задача aiogram (`on_startup`)                      | `bot/app.py` |

**Проверка:** в хендлерах нет бизнес-логики; `IsHost`-фильтр помечен к удалению.

## Этап 3 — Userbot как worker (P0/P1)

| #   | Задача                                                                          | Файлы |
|-----|---------------------------------------------------------------------------------|-------|
| 3.1 | Заменить pyrogram-плагин на воркер: цикл `queue.pop()` вместо `@Client.on_message` | `userbot/worker.py`, удалить `userbot/plugins/` |
| 3.2 | При старте — сброс зависших статусов (или полагаемся на TTL)                     | `userbot/worker.py` |
| 3.3 | Применять `minimal_resolution` через `ydl_opts['format']` (сейчас закомментировано) | `userbot/worker.py` |
| 3.4 | `with open(...)` для видеофайла; удаление файла в `finally`                      | `userbot/worker.py` |
| 3.5 | Типизированная обработка ошибок youtube-dl → структурированный `DownloadResult` с причиной | `userbot/worker.py` |
| 3.6 | Публиковать результат в `ResultBus` вместо отправки текста боту                  | `userbot/worker.py` |

**Проверка:** локально — одно валидное видео и одна битая ссылка доходят до
пользователя с верным сообщением.

## Этап 4 — Чистка и качество (P2/P3)

| #   | Задача                                                                          | Файлы |
|-----|---------------------------------------------------------------------------------|-------|
| 4.1 | Использовать `captions.py` везде, убрать дубли текстов                          | все хендлеры |
| 4.2 | Судьба таблицы `links`: убрать (кэш только в Redis) или оставить как backup с загрузкой в Redis при старте | `utils/db/database.py` |
| 4.3 | Удалить мёртвый код: `IsHost`, неиспользуемые импорты                            | `bot/filters/` |
| 4.4 | Тесты: `IsCorrectLink` (regex), модели транспорта, `download_service` с mock-Redis | `tests/` |
| 4.5 | Обновить `README.md`: запуск через docker-compose, переменная Redis              | `README.md` |
| 4.6 | Логирование вместо `print(str(e))` в userbot                                     | `userbot/worker.py` |

**Проверка:** `pytest` зелёный, `docker-compose up` поднимает всю систему.

## Порядок и риски

1. Этапы последовательны: 0 → 1 → 2/3 (параллельно) → 4.
2. Наибольший риск — этап 3 (смена pyrogram-плагина на воркер). Сначала довести
   этап 1 с юнит-тестами.
3. Этапы 2 и 3 мёржить вместе: старый протокол (dict-как-текст) и новый
   несовместимы, промежуточного рабочего состояния нет. До этого вести работу в `dev`.
4. Миграция данных не требуется: схема `users` не меняется; `links` опционально
   переезжает в Redis (4.2).

## Итоговая структура

```
config/          конфиг (+ redis, абсолютные пути)
loader.py        + redis-клиент
utils/
  db/            SQLite (users)
  transport/     queue, models, result, status, cache   ← НОВОЕ
bot/
  filters/       IsCorrectLink, IsAdmin   (IsHost удалён)
  handlers/      тонкие, без логики
  services/      user_service, download_service          ← НОВОЕ
  result_listener.py                                     ← НОВОЕ
  app.py
userbot/
  worker.py      цикл BRPOP вместо plugins/               ← НОВОЕ
captions.py      используется везде
tests/                                                   ← НОВОЕ
docker-compose.yml, Dockerfile                            ← НОВОЕ
```
