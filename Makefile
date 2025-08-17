# This Makefile provides commands for managing Docker Compose services.
#
# Usage: make [target]
# Run 'make help' to see all available targets.

# Variables
PROJECT_NAME = wipe_out_gmail
COMPOSE_CMD = docker compose -p $(PROJECT_NAME)

# Declare all targets as phony (not file-based)
.PHONY: help ensure-docker up down build logs restart re

# Default target - show help
help: ## Show this help (default target)
	@echo "Usage: make [target]"
	@echo
	@echo "Available targets:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | sort | \
		awk -F':.*?## ' '{printf "  %-20s %s\n", $$1, $$2}'

# Ensure Docker is running before executing Docker commands
# Note: 'open -a Docker' is macOS-specific
# For Linux, use: sudo systemctl start docker
# For Windows/WSL, ensure Docker Desktop is running
ensure-docker:
	@if ! docker info > /dev/null 2>&1; then \
		echo "Docker is not running. Starting Docker..."; \
		open -a Docker; \
		echo "Waiting for Docker to start..."; \
		until docker info > /dev/null 2>&1; do \
			sleep 2; \
		done; \
		echo "Docker is now running."; \
	else \
		echo "Docker is already running."; \
	fi

# Start Docker Compose services in detached mode and show logs
up: ensure-docker ## Start services in detached mode and follow logs
	$(COMPOSE_CMD) up -d
	$(MAKE) logs

# Stop and remove Docker Compose services
down: ensure-docker ## Stop and remove services
	$(COMPOSE_CMD) down

# Build or rebuild Docker Compose services
build: ensure-docker ## Build or rebuild services
	$(COMPOSE_CMD) build

# View real-time logs from containers
logs: ensure-docker ## View real-time logs from containers
	$(COMPOSE_CMD) logs -f

# Restart Docker Compose services (equivalent to down followed by up)
restart: down up ## Restart services (down + up)

# Rebuild and restart services
re: build restart ## Rebuild and restart services (build + restart)