FROM python:3.11-slim

# ffmpeg is required by youtube-dl for muxing video/audio.
# git is required to install youtube-dl from its git source in pyproject.toml.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
    && rm -rf /var/lib/apt/lists/*

# uv — fast dependency manager (replaces pip).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies from the lockfile in a cached layer.
# README.md is referenced by pyproject.toml metadata, so it must be present.
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-cache

# Project code.
COPY . .

# Use the synced virtual environment, and put the project root on the import
# path so both processes can import top-level packages regardless of working_dir.
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
