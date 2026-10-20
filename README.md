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

## LLM

Mỗi role (`planner`, `executor`, `reviewer`) có provider, model và API key riêng trong `.env`:

```
PLANNER_PROVIDER=openai
PLANNER_MODEL=gpt-4o
PLANNER_API_KEY=...
PLANNER_TEMPERATURE=0
```

Tương tự cho `EXECUTOR_*` và `REVIEWER_*`. Provider hỗ trợ: `openai`, `anthropic`, `google_genai`.

```python
from llm.llm import get_planner_llm, get_executor_llm, get_reviewer_llm

llm = get_planner_llm()
llm.invoke("Lập kế hoạch ...")
```
