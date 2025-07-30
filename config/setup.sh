#!/bin/bash

# update package lists
sudo apt update

# install curl if not present
if ! command -v curl &> /dev/null; then
    sudo apt install -y curl
fi

# Download Docker Compose binary
curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o docker-compose

# Make it executable and move to user's bin directory
chmod +x docker-compose
mkdir -p "$HOME/.local/bin"
mv docker-compose "$HOME/.local/bin/docker-compose"

# Add user's bin directory to PATH if not already present
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    export PATH="$HOME/.local/bin:$PATH"
fi

docker-compose build
docker-compose up