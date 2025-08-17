#!/bin/bash

# Create data directory
mkdir -p data/ollama

# Start services
docker-compose up -d

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
sleep 10

# Pull Llama3 model (this will be stored in ./data/ollama)
docker-compose exec ollama ollama pull llama3

echo "Setup complete! Ollama is running with Llama3 model."
echo "API available at: http://localhost:8000"
echo "Ollama direct access: http://localhost:11434"