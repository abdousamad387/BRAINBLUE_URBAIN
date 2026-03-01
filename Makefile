.PHONY: help build up down logs shell test clean deploy docker-build docker-push

# Colors
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m

help:
	@echo "$(BLUE)BRAINBLUE URBAIN - Available Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make build          - Build Docker images"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make logs           - View service logs"
	@echo "  make shell          - Open shell in backend container"
	@echo "  make clean          - Remove containers and volumes"
	@echo ""
	@echo "$(GREEN)Database:$(NC)"
	@echo "  make db-migrate     - Run database migrations"
	@echo "  make db-seed        - Seed database with sample data"
	@echo "  make db-reset       - Reset database (requires confirmation)"
	@echo ""
	@echo "$(GREEN)Testing:$(NC)"
	@echo "  make test           - Run tests"
	@echo "  make test-coverage  - Run tests with coverage"
	@echo "  make lint           - Run linters"
	@echo ""
	@echo "$(GREEN)Production:$(NC)"
	@echo "  make docker-build   - Build production Docker images"
	@echo "  make docker-push    - Push images to registry"
	@echo "  make deploy         - Deploy to production"
	@echo ""

# Development Commands
build:
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker-compose build

up:
	@echo "$(BLUE)Starting services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Services started!$(NC)"
	@echo "Frontend: http://localhost:8000"
	@echo "Backend: http://localhost:5000"
	@echo "PgAdmin: http://localhost:5050"

down:
	@echo "$(BLUE)Stopping services...$(NC)"
	docker-compose down

logs:
	docker-compose logs -f

logs-%:
	docker-compose logs -f $(*)

shell:
	docker-compose exec backend bash

# Database Commands
db-migrate:
	@echo "$(BLUE)Running database migrations...$(NC)"
	docker-compose exec backend python migrate.py upgrade

db-seed:
	@echo "$(BLUE)Seeding database...$(NC)"
	docker-compose exec backend python seeds.py

db-reset:
	@echo "$(RED)⚠️  This will DELETE all data. Type 'yes' to continue:$(NC)"
	@read -r CONFIRM; \
	if [ "$$CONFIRM" = "yes" ]; then \
		docker-compose down -v; \
		docker-compose up -d; \
		echo "$(GREEN)Database reset complete$(NC)"; \
	else \
		echo "$(RED)Cancelled$(NC)"; \
	fi

# Testing Commands
test:
	@echo "$(BLUE)Running tests...$(NC)"
	docker-compose exec backend pytest tests/ -v

test-coverage:
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	docker-compose exec backend pytest tests/ --cov=backend --cov-report=html

lint:
	@echo "$(BLUE)Running linters...$(NC)"
	docker-compose exec backend flake8 backend/
	docker-compose exec backend pylint backend/

# Cleaning Commands
clean:
	@echo "$(BLUE)Cleaning up...$(NC)"
	docker-compose down -v
	@echo "$(GREEN)Cleanup complete$(NC)"

clean-containers:
	docker-compose down

clean-volumes:
	docker volume prune -f

clean-images:
	docker image prune -f

# Production Commands
docker-build:
	@echo "$(BLUE)Building production images...$(NC)"
	docker build -t brainblue:latest .
	docker build -t brainblue-nginx:latest -f Dockerfile.nginx .

docker-push:
	@echo "$(BLUE)Pushing images to registry...$(NC)"
	docker tag brainblue:latest registry.example.com/brainblue:latest
	docker tag brainblue-nginx:latest registry.example.com/brainblue-nginx:latest
	docker push registry.example.com/brainblue:latest
	docker push registry.example.com/brainblue-nginx:latest

deploy:
	@echo "$(BLUE)Deploying to production...$(NC)"
	@if [ -z "$(DEPLOY_ENV)" ]; then \
		echo "$(RED)Error: DEPLOY_ENV not set$(NC)"; \
		exit 1; \
	fi
	@echo "Deploying to $(DEPLOY_ENV)..."
	# Add your deployment script here

# Health check
health:
	@echo "$(BLUE)Checking service health...$(NC)"
	@docker-compose exec backend curl -s http://localhost:5000/api/health || echo "$(RED)Backend is down$(NC)"
	@docker-compose exec postgres pg_isready -U brainblue_user || echo "$(RED)PostgreSQL is down$(NC)"
	@docker-compose exec redis redis-cli ping || echo "$(RED)Redis is down$(NC)"

# Installation
install:
	@echo "$(BLUE)Installing dependencies...$(NC)"
	pip install -r requirements.txt

install-dev:
	@echo "$(BLUE)Installing dev dependencies...$(NC)"
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 pylint

# Setup
setup: build up db-migrate db-seed
	@echo "$(GREEN)Setup complete! BRAINBLUE URBAIN is ready.$(NC)"

# Reset development environment
reset: clean setup
	@echo "$(GREEN)Full reset complete!$(NC)"

# Format code
format:
	@echo "$(BLUE)Formatting code...$(NC)"
	docker-compose exec backend black backend/
	docker-compose exec backend isort backend/

.DEFAULT_GOAL := help
