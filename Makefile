.PHONY: init up down analytics test check smoke logs
init:
	python3 scripts/bootstrap.py
up: init
	docker compose up -d --build --wait --wait-timeout 180
analytics: up
	docker compose --profile analytics up -d --wait --wait-timeout 300
down:
	docker compose --profile analytics down
test:
	docker compose --profile tools build tests
	docker compose --profile tools run --rm tests
check:
	uv run --locked ruff check .
	uv run --locked pytest -q tests/unit
smoke:
	docker compose exec api python -m scripts.smoke
logs:
	docker compose logs --tail 80 api
