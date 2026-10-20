# Multi-Agent

Dự án Multi-Agent, dùng [uv](https://docs.astral.sh/uv/) để quản lý package và PostgreSQL làm database.

## Bắt đầu

```bash
cp .env.example .env     # chỉnh lại thông tin nếu cần
uv sync                  # cài dependencies
docker compose up -d db  # chạy PostgreSQL
uv run python -m db.db   # kiểm tra kết nối database
```

## Chạy toàn bộ bằng Docker

```bash
docker compose up --build
```

## Sử dụng trong code

```python
from db.db import get_session
from sqlalchemy import text

with get_session() as session:
    session.execute(text("SELECT 1"))
```

## Biến môi trường

| Biến                | Mặc định     |
| ------------------- | ------------ |
| `POSTGRES_USER`     | `postgres`   |
| `POSTGRES_PASSWORD` | `postgres`   |
| `POSTGRES_DB`       | `multi_agent`|
| `POSTGRES_HOST`     | `localhost`  |
| `POSTGRES_PORT`     | `5432`       |
