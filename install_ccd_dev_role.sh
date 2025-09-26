#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to print messages
log() {
    echo "INFO: $1"
}

# --- Main Script ---

log "Starting the development environment setup..."

# 1. Check for Debian/Ubuntu distribution
if [ -f /etc/os-release ]; then
    # Source os-release to get OS info
    . /etc/os-release
    if [[ "$ID" == "ubuntu" || "$ID" == "debian" || "$ID_LIKE" == "debian" ]]; then
        log "Debian-based distribution detected: $PRETTY_NAME"
    else
        echo "ERROR: This script is intended for Debian-based distributions (like Ubuntu). Exiting."
        exit 1
    fi
else
    echo "ERROR: /etc/os-release not found. Cannot determine the OS distribution. Exiting."
    exit 1
fi

# 2. Update apt and install prerequisites
log "Updating package list and installing git and ansible..."
sudo apt-get update
sudo apt-get install -y git ansible

# 3. Clone the repository and run the playbook
REPO_URL="https://github.com/fchicout/prep-devsecops-pc.git"
REPO_DIR="prep-devsecops-pc"
log "Cloning repository from $REPO_URL..."
git clone --recurse-submodules "$REPO_URL"
cd "$REPO_DIR"
log "Running the Ansible playbook..."
ansible-playbook main.yml --ask-become-pass -i inventory.ini

# 4. Remove the cloned repository
cd ..
log "Removing the cloned repository..."
rm -rf "$REPO_DIR"  