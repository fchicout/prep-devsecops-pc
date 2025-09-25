#!/bin/bash
#
# This script automates the process of setting up the Python environment,
# running Molecule tests for the Ansible role, and serving the Allure test report.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- 1. Setup Python Virtual Environment ---
VENV_DIR=".venv"

echo "--- Checking for Python virtual environment ---"
if [ ! -d "$VENV_DIR" ]; then
  echo "Virtual environment not found. Creating it at '$VENV_DIR'..."
  python3 -m venv "$VENV_DIR"
else
  echo "Virtual environment already exists."
fi

# --- 2. Activate Virtual Environment and Install Dependencies ---
echo "--- Activating virtual environment and installing dependencies ---"
source "$VENV_DIR/bin/activate"
pip install -r requirements.txt

# --- 3. Run Molecule Tests ---
echo "--- Changing to the Ansible role directory to run Molecule ---"
cd ccd_dev_tools

# Pass the allure_report_dir variable to molecule, which forwards it to pytest
molecule test -s qemu -- -e allure_report_dir=./molecule/qemu/.allure/results

echo "--- Starting Molecule test suite for the 'qemu' scenario ---"
echo "--- Molecule tests completed successfully ---"

# --- 4. Serve Allure Report ---
echo "--- Changing back to the project root ---"
cd ..

echo "--- Starting Allure report server ---"
# The 'allure serve' command is blocking. It will start a local web server,
# open the report in your default browser, and the script will pause here.
# Press Ctrl+C in the terminal to stop the server and exit the script.
allure serve ccd_dev_tools/molecule/qemu/.allure/results