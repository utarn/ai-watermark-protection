# Docker Setup Guide

This guide explains how to run the AI Watermark Fighter application using Docker.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

### Installing Docker

**macOS:**
- Download and install [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)

**Windows:**
- Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
```

## Quick Start

### 1. Build and Start the Container

```bash
# Build the image and start the container in detached mode
docker-compose up -d
```

This will:
- Build the Docker image with Python 3.11 and uv 0.9.0
- Install all project dependencies
- Start the Gradio application on port 7860

### 2. Access the Application

Open your web browser and navigate to:
```
http://localhost:7860
```

### 3. View Logs

To see the application logs in real-time:
```bash
docker-compose logs -f
```

Press `Ctrl+C` to stop viewing logs (container will continue running).

### 4. Stop the Container

```bash
docker-compose down
```

## Common Commands

### View Running Containers
```bash
docker-compose ps
```

### Restart the Container
```bash
docker-compose restart
```

### Rebuild After Code Changes
```bash
docker-compose up -d --build
```

### Stop and Remove Everything
```bash
docker-compose down --volumes --remove-orphans
```

### View Container Resource Usage
```bash
docker stats ai-watermark-fighter
```

### Execute Commands Inside Container
```bash
# Open a shell inside the container
docker-compose exec ai-watermark-fighter bash

# Run tests
docker-compose exec ai-watermark-fighter uv run pytest

# Check uv version
docker-compose exec ai-watermark-fighter uv --version
```

## Development Workflow

The `docker-compose.yml` includes volume mounts for development:
- `./app.py:/app/app.py` - Changes to app.py are reflected immediately
- `./test_logic.py:/app/test_logic.py` - Changes to test_logic.py are reflected immediately

To see changes:
1. Edit your code locally
2. Restart the container: `docker-compose restart`

## Configuration

### Change Port

Edit `docker-compose.yml` to use a different port:
```yaml
ports:
  - "8080:7860"  # Access at http://localhost:8080
```

### Environment Variables

Add or modify environment variables in `docker-compose.yml`:
```yaml
environment:
  - GRADIO_SERVER_NAME=0.0.0.0
  - GRADIO_SERVER_PORT=7860
  - YOUR_CUSTOM_VAR=value
```

## Dockerfile Details

The Dockerfile:
- Uses Python 3.11 slim base image
- Installs uv version 0.9.0
- Copies project files and installs dependencies
- Exposes port 7860 for Gradio
- Runs the application with `uv run python app.py`

## Troubleshooting

### Port Already in Use
```bash
# Find what's using port 7860
lsof -i :7860  # macOS/Linux
netstat -ano | findstr :7860  # Windows

# Change port in docker-compose.yml or stop the conflicting service
```

### Container Fails to Start
```bash
# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Permission Issues (Linux)
```bash
# Add your user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or run with sudo
sudo docker-compose up -d
```

### Image Size Issues
```bash
# Clean up unused Docker resources
docker system prune -a

# View image size
docker images | grep ai-watermark-fighter
```

## Health Check

The container includes a health check that:
- Tests the application every 30 seconds
- Times out after 10 seconds
- Retries 3 times before marking as unhealthy
- Waits 40 seconds after start before first check

Check health status:
```bash
docker-compose ps
# Look for "healthy" status
```

## Production Deployment

For production use:

1. Remove volume mounts from `docker-compose.yml`
2. Set appropriate resource limits:
```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
```

3. Use environment-specific configurations:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

4. Consider using a reverse proxy (nginx, traefik) for SSL/TLS

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Gradio Documentation](https://gradio.app/docs/)
- [UV Documentation](https://github.com/astral-sh/uv)