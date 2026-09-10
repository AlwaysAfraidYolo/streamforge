# Версии и совместимость

Проверка источников 10 сентября 2026 года. Образы не используют latest.

- API: Python 3.14.7, Debian bookworm slim. Локально установлен 3.14.3;
  зависимости разрешены для ветки 3.14. Системный Python не изменён.
- PostgreSQL 17.11: поддерживаемая ветка, один major для приложения и Airflow.
  Это отдельные контейнеры и volumes, а не общая БД с бизнес-данными.
- Redis 8.8.2: только кэш; постоянное хранение выключено намеренно.
- SeaweedFS 4.46: официальный образ chrislusf/seaweedfs, локальный режим mini,
  S3 v4, path-style. Bucket streamforge-raw создаётся автоматически.
- ClickHouse 26.8.2.7: LTS-ветка; в каркасе только проверка доступности.
- Airflow 3.3.1, официальный образ с Python 3.12 и штатными зависимостями.
  Он изолирован от API. Не устанавливаем Airflow в Python-окружение приложения.
  Standalone + LocalExecutor предназначены для этого локального обучения.

Точные версии библиотек API: pyproject.toml; полный граф: uv.lock.
requirements.lock и requirements-dev.lock экспортированы с SHA-256 hashes.
Обновлять lock-файлы нужно одновременно и повторять проверки.

## Почему заменён MinIO

Официальный MinIO Community архивирован 25 апреля 2026 года и помечен
как неподдерживаемый. Пользователь согласовал поддерживаемую замену.
Архитектурная роль raw zone и S3 API остаются прежними.
Документы Roadmap и Execution Plan, созданные ранее, ещё называют MinIO;
для текущего окружения это следует читать как S3 / SeaweedFS.

## Официальные источники

- https://www.postgresql.org/support/versioning/
- https://hub.docker.com/_/python
- https://hub.docker.com/_/redis
- https://github.com/seaweedfs/seaweedfs/releases/tag/4.46
- https://github.com/seaweedfs/seaweedfs/wiki/Quick-Start-with-weed-mini
- https://github.com/minio/minio
- https://packages.clickhouse.com/
- https://airflow.apache.org/docs/apache-airflow/3.3.1/installation/prerequisites.html
- https://airflow.apache.org/docs/apache-airflow/3.3.1/howto/docker-compose/index.html

Практическую совместимость подтверждают только результаты запуска и тестов,
которые записываются в VERIFICATION.md. ARM64 проверяется на Mac; AMD64 в CI
считается проверенным только после успешного удалённого CI run.
