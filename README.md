# StreamForge

Учебная платформа данных для развития в Data Platform Engineer.
Сейчас готовится фундамент: контейнеры, структура Python-проекта, проверка
зависимостей и рабочее окружение. Бизнес-логику реализуем небольшими задачами.

Начни с [инструкции запуска](docs/START_HERE.md).

## Целевая архитектура

```text
Sources → FastAPI ingestion
             ├─ PostgreSQL: метаданные
             ├─ S3 / SeaweedFS: исходные данные
             └─ Redis: восстанавливаемый кэш
                       ↓
                Airflow / Python ETL
                       ↓
                ClickHouse marts
                       ↓
                FastAPI analytics
```

## Что есть в стартовом каркасе

- FastAPI с `/live`, `/ready` и OpenAPI.
- SQLAlchemy async engine и Alembic baseline без бизнес-таблиц.
- PostgreSQL, Redis и локальный S3 endpoint с постоянным raw storage.
- ClickHouse и Airflow отдельным Compose-профилем `analytics`.
- Smoke-проверки записи/чтения и CI-конфигурация.
- Точные версии Python-пакетов, `uv.lock` и requirements с hashes.

Не реализованы: приём событий, идемпотентность, worker, ETL, DQ и витрины.
Папки под них уже созданы; они станут учебными этапами.

## Структура

```text
app/                 API, конфигурация, модели и доступ к данным
worker/              будущий фоновый обработчик
pipelines/           будущие ETL-функции
dags/                Airflow, пока только smoke DAG
migrations/          Alembic
sql/clickhouse/      будущие таблицы и витрины
tests/               тесты
scripts/             bootstrap и smoke
docs/                запуск и решения по инфраструктуре
```

## Команды

```sh
make up
make smoke
make test
make analytics
make down
```

Все опубликованные порты привязаны к `127.0.0.1`. Это локальный стенд,
не конфигурация для публичного сервера. Redis используется как непостоянный
кэш; PostgreSQL и S3 имеют Docker volumes. Образы приложений используют
непривилегированного пользователя. `.env` не коммитится.
