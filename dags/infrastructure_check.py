"""Manual smoke DAG. Business ETL will be written during mentoring."""

from datetime import UTC, datetime

from airflow.sdk import dag, task


@dag(
    dag_id="infrastructure_check",
    schedule=None,
    start_date=datetime(2026, 1, 1, tzinfo=UTC),
    catchup=False,
    max_active_runs=1,
    tags=["infrastructure"],
)
def infrastructure_check():
    @task
    def check():
        import urllib.request

        with urllib.request.urlopen("http://api:8000/ready", timeout=10) as response:
            assert response.status == 200

    check()


infrastructure_check()
