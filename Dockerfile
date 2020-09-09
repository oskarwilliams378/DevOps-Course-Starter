FROM python:3.8.1-buster as base
RUN pip install poetry
EXPOSE 8000
WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN poetry install --no-root --no-dev

FROM base as prod
COPY . /code/
ENTRYPOINT poetry run gunicorn "app:create_app()" --bind 0.0.0.0:8000

FROM base as dev
ENTRYPOINT poetry run flask run -h 0.0.0.0 -p 8000