#!/bin/bash
#
# This script automates setting up the Python environment,
# running Molecule tests for the Ansible role, and serving the Allure test report.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- 1. Setup Python Virtual Environment ---
VENV_DIR=".venv"
ALLURE_RESULTS_DIR="ccd_dev_tools/molecule/qemu/.allure/results"

echo "--- [1/5] Cleaning up previous virtual environment ---"
rm -rf "$VENV_DIR"

echo "--- [2/5] Creating new Python virtual environment at '$VENV_DIR' ---"
python3 -m venv "$VENV_DIR"

# --- 2. Activate Environment and Install Dependencies ---
echo "--- [3/5] Activating virtual environment and installing dependencies ---"
source "$VENV_DIR/bin/activate"
pip install -r requirements.txt

# --- 3. Run Molecule Tests ---
echo "--- [4/5] Running Molecule tests for the 'qemu' scenario ---"

# Ensure the Allure results directory is clean before running tests.
echo "Clearing old Allure test results..."
rm -rf "$ALLURE_RESULTS_DIR"
mkdir -p "$ALLURE_RESULTS_DIR"

# Change to the role directory to execute Molecule.
cd ccd_dev_tools

# The allure_report_dir variable is passed to molecule, which forwards it to pytest.
# The path is relative to the current directory (`ccd_dev_tools`).
molecule test -s qemu -- -e allure_report_dir=./molecule/qemu/.allure/results

# --- 4. Serve Allure Report ---
# Change back to the project root directory.
cd ..

echo "--- [5/5] Serving Allure test report ---"
# The 'allure serve' command is blocking. It will start a local web server,
# open the report in your default browser, and the script will pause here.
# Press Ctrl+C in the terminal to stop the server and exit the script.
allure serve "$ALLURE_RESULTS_DIR"