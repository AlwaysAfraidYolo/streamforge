FROM python:3.14.7-slim-bookworm AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /workspace
COPY requirements.lock /tmp/requirements.lock
RUN pip install --no-cache-dir --require-hashes -r /tmp/requirements.lock \
 && useradd --create-home --uid 10001 app
COPY --chown=app:app app ./app
COPY --chown=app:app scripts ./scripts
COPY --chown=app:app migrations ./migrations
COPY --chown=app:app alembic.ini ./alembic.ini
USER app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS test
ENV RUFF_CACHE_DIR=/tmp/ruff-cache PYTEST_ADDOPTS="-o cache_dir=/tmp/pytest-cache"
USER root
COPY requirements-dev.lock /tmp/requirements-dev.lock
RUN pip install --no-cache-dir --require-hashes -r /tmp/requirements-dev.lock
COPY --chown=app:app tests ./tests
COPY --chown=app:app pyproject.toml ./pyproject.toml
USER app
CMD ["pytest", "-q"]
