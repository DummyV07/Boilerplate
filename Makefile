.PHONY: install install-dev check fix dev docker-build docker-up docker-down web-dev web-build web-check test deploy health-check

install:
	cd backend && uv sync --no-dev

install-dev:
	cd backend && uv sync --extra dev
	cd frontend && npm ci

check:
	cd backend && uv run ruff check app tests
	cd backend && uv run ruff format --check app tests
	cd backend && uv run mypy app

fix:
	cd backend && uv run ruff check --fix app tests
	cd backend && uv run ruff format app tests

dev:
	@echo "启动后端 (8000) 与前端 (3000)，请分别在两个终端运行："
	@echo "  make dev-backend"
	@echo "  make dev-frontend"

dev-backend:
	cd backend && uv run python run.py

dev-frontend:
	cd frontend && npm run dev

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

web-dev:
	cd frontend && npm run dev

web-build:
	cd frontend && npm run build

web-check:
	cd frontend && npm run build

test:
	cd backend && uv run pytest tests/ -v

deploy:
	./scripts/deploy.sh

health-check:
	./scripts/health-check.sh
