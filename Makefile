# Makefile for Engineericly Feed Docker Management

.PHONY: help build up down restart logs shell clean migrate collectstatic createsuperuser

# Default target
help:
	@echo "Available commands:"
	@echo "  build     - Build Docker images"
	@echo "  up        - Start development environment"
	@echo "  down      - Stop and remove containers"
	@echo "  restart   - Restart services"
	@echo "  logs      - Show logs"
	@echo "  shell     - Open shell in web container"
	@echo "  clean     - Clean up containers and volumes"
	@echo "  migrate   - Run Django migrations"
	@echo "  collectstatic - Collect static files"
	@echo "  createsuperuser - Create Django superuser"

# Build images
build:
	docker-compose build

# Start development environment
up:
	docker-compose up -d

# Update and restart services
update:
	docker-compose down && docker-compose up -d --build

# Stop services
down:
	docker-compose down

# Restart services
restart:
	docker-compose restart

# Show logs
logs:
	docker-compose logs -f

# Open shell in web container
shell:
	docker-compose exec web bash

# Run Django migrations
migrate:
	docker-compose exec web python manage.py migrate

# Collect static files
collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

# Create superuser
createsuperuser:
	docker-compose exec web python manage.py createsuperuser

# Clean up everything
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

# Install dependencies (for local development)
install:
	pip install -r requirements.txt

# Run tests
test:
	docker-compose exec web python manage.py test
