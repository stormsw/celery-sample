FROM python:3.7.6-slim-buster
WORKDIR /app/test_celery 

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.3
RUN pip install poetry==${POETRY_VERSION}
COPY poetry.lock pyproject.toml ./
RUN POETRY_VIRTUALENVS_CREATE=false poetry install
# --no-root
COPY . .
WORKDIR /app
CMD ["celery", "worker", "-A", "test_celery.app",  "--loglevel=info"]
#ENTRYPOINT [ "poetry run celery worker -A test_celery.app --loglevel=info" ]