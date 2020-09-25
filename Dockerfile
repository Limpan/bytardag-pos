FROM python:3.8.5-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv

WORKDIR /app


# 'builder' stage for building package and preparing venv.
FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.0.10


RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    curl

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | pip install -r /dev/stdin

COPY . .
RUN poetry build && pip install dist/*.whl


# Build 'final' stage
FROM base as final
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "-w 4", "-b :8000", "wsgi:app"]