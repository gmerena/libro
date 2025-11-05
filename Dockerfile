FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ENV TZ="Europe/Budapest" \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN apt-get update && \
    apt-get install -y --no-install-recommends util-linux tzdata libpq-dev libmagic1 file && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "export PS1='[\033[01;32m]\u@\h:[\033[01;34m]\w[\033[00m]$ '" >> ~/.bashrc

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]             