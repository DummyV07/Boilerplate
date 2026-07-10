.PHONY: install install-dev dev docker-build docker-up docker-down web-dev web-build web-check deploy health-check

# 不生成 __pycache__ 字节码目录
export PYTHONDONTWRITEBYTECODE := 1

install:
	cd backend && uv sync

install-dev:
	cd backend && uv sync
	cd frontend && npm ci

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

deploy:
	./scripts/deploy.sh

health-check:
	./scripts/health-check.sh
