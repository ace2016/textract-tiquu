#!/bin/bash

# Stop and remove containers
docker-compose down

# Optional: Remove downloaded models (uncomment if you want to clean everything)
# rm -rf data/ollama

echo "Cleanup complete!"