# Start the Docker Compose services
up:
	docker-compose up -d

# Stop the Docker Compose services
down:
	docker-compose down

# Build or rebuild services
build:
	docker-compose build

# View output from containers
logs:
	docker-compose logs -f

# Restart the Docker Compose services
restart: down up
