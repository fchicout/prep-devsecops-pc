# Role: ccd_dev_tools

This Ansible role automates the setup of a complete development environment on Debian-based systems (e.g., Ubuntu, Debian). It is designed to provision a machine with the essential tools required for a modern DevSecOps workflow, handling everything from system updates to the installation of containerization and virtualization software.

## Requirements

This role is designed to run on **Debian-based** Linux distributions (e.g., Ubuntu, Debian).

The target machine must have `sudo` access for the user running the playbook, as the role needs to install packages and manage system configuration.

## What This Role Does

The role executes a series of tasks in a logical order to ensure a stable and consistent setup:

1.  **System Preparation (`_setup_system.yml`)**
    *   Updates the `apt` package cache.
    *   Upgrades all installed packages to their latest available versions.

2.  **Install Prerequisites (`_setup_prereqs.yml`)**
    *   Installs essential command-line tools and libraries required by other software, such as `curl`, `git`, `python3-pip`, `htop`, and `gnupg`.
    *   Ensures a clean state by removing potentially conflicting repository files before adding new ones.

3.  **Install Ansible-related Tools (`_install_ansible_tools.yml`)**
    *   Installs `ansible-lint` and `yamllint` via `pip`. These linters are crucial for maintaining high-quality Ansible content and YAML files.

4.  **Install Docker (`_install_docker.yml`)**
    *   Securely adds the official Docker GPG key to the system's keyring.
    *   Configures the official Docker `apt` repository.
    *   Installs the complete Docker suite: Docker Engine (`docker-ce`), CLI (`docker-ce-cli`), `containerd.io`, and the Docker Compose plugin.
    *   Adds the current user to the `docker` group to allow running Docker commands without `sudo`. **Note:** The user will need to log out and log back in for this change to take effect.

5.  **Install VirtualBox (`_install_virtualbox.yml`)**
    *   Adds the official Oracle GPG key and `apt` repository.
    *   Installs a specific, stable version of VirtualBox (`virtualbox-7.0`) to ensure compatibility and predictable behavior.

6.  **Install Vagrant (`_install_vagrant.yml`)**
    *   Adds the official HashiCorp GPG key and `apt` repository.
    *   Installs Vagrant.

7.  **Install Visual Studio Code (`_install_vscode.yml`)**
    *   Adds the official Microsoft GPG key and `apt` repository.
    *   Installs Visual Studio Code.

## Role Variables

This role does not require any specific variables to be set by the user. It is designed to work out-of-the-box.


## Testing

This role uses **Molecule** and **Testinfra** to perform integration testing. The tests are designed to run against a virtual machine to verify that the role has configured the system correctly. The primary test suite can be executed via the `run_tests.sh` script.

Below is a summary of the automated tests for each component.

### Docker (`test_docker.py`)

*   **Test Case 1: `test_docker_gpg_key_properties`**: Verifies that the Docker GPG key exists at `/etc/apt/keyrings/docker.gpg`, is owned by `root`, and is not an empty file.
*   **Test Case 2: `test_docker_apt_repository_configured`**: Confirms that the system's package manager (`apt`) is aware of the official Docker repository by checking the output of `apt-cache policy`.
*   **Test Case 3: `test_docker_packages_are_installed`**: Checks that all required Docker packages (`docker-ce`, `docker-ce-cli`, `containerd.io`, `docker-compose-plugin`) are installed.
*   **Test Case 4: `test_docker_service_is_running_and_enabled`**: Ensures the `docker` service is both currently running and enabled to start on system boot.
*   **Test Case 5: `test_docker_commands_are_functional`**: Verifies that the `docker --version` and `docker compose version` commands execute successfully.
*   **Test Case 6: `test_docker_daemon_is_accessible`**: Checks that the Docker CLI can communicate with the Docker daemon by running `sudo docker info`.
*   **Test Case 7: `test_docker_group_and_socket_permissions`**: Confirms that the `docker` group has been created and that it is the group owner of the Docker socket file (`/var/run/docker.sock`).

### VirtualBox (`test_virtualbox.py`)

*   **Test Case 1: `test_virtualbox_gpg_key_properties`**: Verifies that the Oracle VirtualBox GPG key exists at `/etc/apt/keyrings/oracle-virtualbox-2016.gpg`, is owned by `root`, and is not empty.
*   **Test Case 2: `test_virtualbox_package_is_installed`**: Checks that the `virtualbox-7.0` package is successfully installed.
*   **Test Case 3: `test_vboxmanage_command_is_functional`**: Ensures the `VBoxManage` command-line tool is available and functional by running `VBoxManage --version` and checking that it reports the expected version (7.0).

### Vagrant (`test_vagrant.py`)

*   **Test Case 1: `test_hashicorp_gpg_key_properties`**: Verifies that the HashiCorp GPG key exists, is owned by `root`, and is not empty.
*   **Test Case 2: `test_hashicorp_apt_repository_configured`**: Confirms that the HashiCorp `apt` repository file exists and is correctly configured with the GPG key.
*   **Test Case 3: `test_vagrant_package_is_installed`**: Checks that the `vagrant` package is successfully installed.
*   **Test Case 4: `test_vagrant_command_is_functional`**: Ensures the `vagrant` command is in the system's PATH and that `vagrant --version` executes successfully.

### Prerequisites (`test_prereqs.py`)

*   **Test Case 1: `test_keyrings_directory_properties`**: Ensures the `/etc/apt/keyrings` directory exists with the correct permissions and ownership (`root:root`, `0755`).
*   **Test Case 2: `test_prereq_packages_are_installed`**: Verifies that a list of essential packages (like `curl`, `git`, `python3-pip`, etc.) are all installed.
*   **Test Case 3: `test_prereq_commands_are_available` & `test_prereq_commands_are_functional`**: Confirms that the executables for the prerequisite packages are in the system's PATH and are functional by running a simple version or help command.

### Ansible Tools (`test_ansible_tools.py`)

*   **Test Case 1: `test_ansible_tool_packages_are_installed`**: Verifies that `ansible-lint` and `yamllint` are installed.
*   **Test Case 2 & 3: `test_ansible_tool_commands_are_available` & `test_ansible_tool_commands_are_functional`**: Checks that the `ansible-lint` and `yamllint` commands are in the PATH and can be executed successfully.

### Allure Framework (`test_allure.py`)

*   **Test Case 1: `test_java_package_is_installed` & `test_java_command_is_functional`**: Verifies that a Java Development Kit (`default-jdk`) is installed and that the `java` command is functional, as it is a dependency for Allure.
*   **Test Case 2: `test_allure_package_is_installed` & `test_allure_command_is_functional`**: Confirms that the `allure` package is installed and that the `allure --version` command works correctly.

## Dependencies

This role has no dependencies on other Ansible Galaxy roles.

## Example Playbook

You can use this role in your own playbook to set up a machine.

1.  Create an inventory file (e.g., `inventory.ini`):

    ```ini
    [workstation]
    localhost ansible_connection=local
    ```

2.  Create a playbook file (e.g., `main.yml`):

    ```yaml
    ---
    - name: Setup Development Workstation
      hosts: workstation
      become: yes
      roles:
        - ccd_dev_tools
    ```

3.  Run the playbook:

    ```bash
    ansible-playbook main.yml -i inventory.ini --ask-become-pass
    ```

    The `--ask-become-pass` flag will prompt you for your `sudo` password to perform the installation tasks.

## Standalone Execution

This repository includes a convenience script, `install.sh`, to bootstrap the entire process on a fresh machine. It will install Ansible and then execute the playbook automatically.

To run it, simply execute the following commands in your terminal:

```bash
# 1. Download the script
curl -O https://raw.githubusercontent.com/fchicout/prep-devsecops-pc/main/install.sh

# 2. Make it executable
chmod +x install.sh

# 3. Run the script
./install.sh
```

The script will handle checking the OS, installing Ansible, cloning the repository, and running the playbook for you.

## License

MIT

## Author Information

This role was created by fchicout.
