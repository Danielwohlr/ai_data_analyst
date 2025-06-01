FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install uv and sync dependencies into .venv
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen

# Copy application code (or let docker-compose mount it)
COPY . /app

# Prepend .venv/bin so that uvicorn (and other scripts) are on PATH
ENV PATH="/app/.venv/bin:$PATH"

# Use uvicorn from the venv
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
