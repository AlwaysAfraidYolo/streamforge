# Проверка стартового окружения

Проверено 11 сентября 2026 года на Mac ARM64 с Docker Desktop 29.4.2.

- Compose запустил API, PostgreSQL, Redis, SeaweedFS, ClickHouse,
  Airflow и отдельную metadata database Airflow.
- `/live` и `/ready` доступны. `/ready` проверяет PostgreSQL и S3.
- Smoke: запись и чтение временной таблицы PostgreSQL, Redis-ключа и S3-объекта;
  SELECT 1 в ClickHouse. Все проверки прошли; тестовые объекты удалены.
- Alembic применил baseline `0001`, текущая версия — head.
- Три unit-теста прошли локально на Python 3.14.3 и внутри контейнера
  на Python 3.14.7. Ruff прошёл в обоих окружениях.
- `pip check` для API и Airflow не обнаружил конфликтующих зависимостей.
- Airflow не сообщает об ошибках импорта DAG. `airflow dags test
  infrastructure_check` завершился со статусом success.
- При остановке S3 `/ready` вернул HTTP 503 с `s3=unavailable`;
  после включения S3 вернулся HTTP 200 с обоими checks=ok.

Это проверка инфраструктуры. Ingestion, worker, ETL и витрины ещё не реализованы.
Удалённый GitHub Actions run и AMD64 пока не проверены: требуется завершить вход
в GitHub и публикацию репозитория.

## Повторить проверки

```sh
make up
make test
make smoke
make analytics
docker compose exec api alembic upgrade head
docker compose exec api python -m scripts.smoke --analytics
docker compose exec airflow airflow dags test infrastructure_check
```
