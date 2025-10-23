# Multi-stage Dockerfile for DeFi Portfolio Agent

# Stage 1: Base Python image
FROM python:3.11-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

# Stage 2: Node.js base for TypeScript packages
FROM node:18-alpine as node-base

WORKDIR /app

# Stage 3: Python dependencies
FROM python-base as python-deps

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 4: TypeScript build
FROM node-base as ts-build

COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile

COPY tsconfig.json ./
COPY mcp-servers/ ./mcp-servers/
RUN pnpm build

# Stage 5: Final API image
FROM python-base as api

# Copy Python dependencies
COPY --from=python-deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code
COPY api/ ./api/
COPY tools/ ./tools/
COPY config/ ./config/
COPY .env.example ./.env

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 6: MCP Servers image
FROM node-base as mcp-servers

COPY --from=ts-build /app/node_modules ./node_modules
COPY --from=ts-build /app/mcp-servers ./mcp-servers

EXPOSE 3001 3002 3003

CMD ["node", "mcp-servers/start-all.js"]

# Stage 7: UI (Next.js) image
FROM node-base as ui

COPY ui/package.json ui/pnpm-lock.yaml ./ui/
WORKDIR /app/ui
RUN npm install -g pnpm && pnpm install --frozen-lockfile

COPY ui/ .
RUN pnpm build

EXPOSE 3000

CMD ["pnpm", "start"]
