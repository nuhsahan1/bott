.PHONY: help up down logs test lint format clean

help:
	@echo "Bott - Multi-Bot Telegram Orchestration Platform"
	@echo ""
	@echo "Available commands:"
	@echo "  make up              - Start all services"
	@echo "  make down            - Stop all services"
	@echo "  make logs            - View all service logs"
	@echo "  make logs-gateway    - View gateway logs"
	@echo "  make logs-flow       - View flow engine logs"
	@echo "  make rebuild         - Rebuild all Docker images"
	@echo "  make clean           - Remove all containers, volumes, and cache"
	@echo "  make test            - Run tests"
	@echo "  make lint            - Run linters"
	@echo "  make format          - Format code"
	@echo "  make shell-gateway   - Open shell in gateway container"
	@echo "  make shell-postgres  - Open psql in postgres container"
	@echo "  make db-migrate      - Run database migrations"

up:
	docker-compose up -d
	@echo "Services starting. Check logs with: make logs"

down:
	docker-compose down
	@echo "Services stopped"

logs:
	docker-compose logs -f

logs-gateway:
	docker-compose logs -f gateway

logs-flow:
	docker-compose logs -f flow-engine

rebuild:
	docker-compose build --no-cache
	docker-compose up -d

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

test:
	docker-compose exec gateway pytest tests/ -v

lint:
	docker-compose exec gateway flake8 .
	docker-compose exec gateway pylint app/

format:
	docker-compose exec gateway black .
	docker-compose exec gateway isort .

shell-gateway:
	docker-compose exec gateway /bin/bash

shell-postgres:
	docker-compose exec postgres psql -U postgres -d bott

db-migrate:
	docker-compose exec gateway alembic upgrade head

.DEFAULT_GOAL := help
