FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY . .
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "python", "-m", "db.db"]
