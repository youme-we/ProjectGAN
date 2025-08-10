# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY . .

RUN uv sync --locked

ENV PROJECT_NAME="GAN1"
ENV PORT_NN=3002

EXPOSE 3002

CMD ["uv", "run", "main.py"]
