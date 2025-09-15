# Development Environment Setup using Ansible

This project provides an automated way to set up a complete development environment on a Debian-based Linux system (like Ubuntu) using Ansible. It's designed to be idempotent and repeatable, ensuring a consistent setup every time.

## Project Structure

The project is composed of the following key parts:

-   `main.yml`: The main Ansible playbook that orchestrates the setup process.
-   `inventory.ini`: The Ansible inventory file, configured to run on the local machine.
-   `install.sh`: A bootstrap script to set up a fresh machine by installing Ansible and running the playbook.
-   `run_tests.sh`: A script to automate the testing of the Ansible role using Molecule and Allure.
-   `roles/`: This directory contains the Ansible roles.
    -   `ccd_dev_tools`: The primary role that installs and configures all the development tools.

## What Gets Installed?

The `ccd_dev_tools` Ansible role will set up the following software:

-   **System Tools**: `git`, `curl`, `htop`, `python3-pip`, and other essentials.
-   **Ansible Linting**: `ansible-lint` and `yamllint` for code quality.
-   **Containerization**: Docker Engine, Docker CLI, and Docker Compose.
-   **Virtualization**: VirtualBox and Vagrant.
-   **Code Editor**: Visual Studio Code.
-   **Test Reporting**: Allure Framework CLI.

For more details on the role itself, see the `ccd_dev_tools/README.md`.

---

## How to Use

There are two main ways to use this project: setting up a new machine or running the tests for development.

### 1. Setting Up a New Development Machine

If you are on a fresh Debian-based system (like Ubuntu) and want to set up your development environment, the `install.sh` script automates the entire process.

**Prerequisites:**
-   A Debian-based Linux distribution.
-   `sudo` access.

**Instructions:**

1.  **Download the script:**
    ```bash
    curl -O https://raw.githubusercontent.com/fchicout/prep-devsecops-pc/main/install.sh
    ```

2.  **Make it executable:**
    ```bash
    chmod +x install.sh
    ```

3.  **Run the script:**
    ```bash
    ./install.sh
    ```

The script will first install Ansible, then clone this repository and run the main playbook. You will be prompted for your `sudo` password to allow system-level changes.

### 2. Running the Test Suite

If you are developing the Ansible role and want to run the integration tests, use the `run_tests.sh` script. This script uses Molecule to create a test instance, applies the Ansible role, runs verification tests, and finally serves an Allure test report.

**Prerequisites:**
-   You have cloned this repository.
-   You have `python3` and `python3-venv` installed.
-   Your system supports QEMU/KVM for the test environment.

**Instructions:**

1.  **Make the script executable:**
    ```bash
    chmod +x run_tests.sh
    ```

2.  **Run the script from the project root:**
    ```bash
    ./run_tests.sh
    ```

The script will automatically:
1.  Create a Python virtual environment (`.venv`).
2.  Install all required dependencies from `requirements.txt`.
3.  Execute the full `molecule test` lifecycle for the `qemu` scenario.
4.  Once tests are complete, it will launch the Allure web server to display the test results in your browser. You can stop the server by pressing `Ctrl+C` in your terminal.