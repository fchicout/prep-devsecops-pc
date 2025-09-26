#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to print messages
log() {
    echo "======================================================================"
    echo "INFO: $1"
    echo "======================================================================"
}

log "Starting full environment setup..."

log "Running the development environment setup..."
./install_ccd_dev_role.sh

log "Running the base hardening setup..."
./install_base_hardening_role.sh

log "All setup scripts have been executed successfully."