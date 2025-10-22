FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.7.8 /uv /uvx /bin/

ENV TZ="Europe/Budapest" \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends util-linux tzdata libpq-dev libmagic1 file && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "export PS1='[\033[01;32m]\u@\h:[\033[01;34m]\w[\033[00m]$ '" >> ~/.bashrc

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY . .

ENV PATH="/app/.venv/bin/:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]