# This Makefile provides commands for managing Docker Compose services.
#
# Available targets:
#
# up        - Start Docker Compose services in detached mode and show logs
# down      - Stop and remove Docker Compose services
# build     - Build or rebuild Docker Compose services
# logs      - View real-time logs from containers
# restart   - Restart Docker Compose services (equivalent to down followed by up)
# Start the Docker Compose services
up: 
	docker compose -p wipe_out_gmail up -d
	$(MAKE) logs

# Stop the Docker Compose services
down:
	docker compose -p wipe_out_gmail down

# Build or rebuild services
build:
	docker compose -p wipe_out_gmail build

# View output from containers
logs:
	docker compose -p wipe_out_gmail logs -f

# Restart the Docker Compose services
restart: down up

# Rebuild and restart services
re: build restart