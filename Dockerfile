FROM python:3.11-slim

WORKDIR /app

ENV FLASK_APP=encontros
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

COPY . /app

RUN apt update && apt install -qy libpq-dev python-dev-is-python3 gcc
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
RUN chmod +x ./entrypoint.sh
CMD ["./entrypoint.sh"]