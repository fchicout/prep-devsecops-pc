# Role: ccd_dev_tools

This role automates the setup of a complete development environment on Debian-based systems (like Ubuntu). It handles system updates, prerequisite installation, and the setup of essential tools for a DevSecOps workflow.

## Requirements

This role is designed to run on **Debian-based** Linux distributions (e.g., Ubuntu, Debian).

The target machine must have `sudo` access for the user running the playbook, as the role needs to install packages and manage system configuration.

## What This Role Does

The role is broken down into logical steps to configure the system:

1.  **System Preparation (`_setup_system.yml`)**
    *   Updates the `apt` package cache.
    *   Upgrades all installed packages to their latest versions (`apt upgrade dist`).

2.  **Install Prerequisites (`_setup_prereqs.yml`)**
    *   Installs essential command-line tools and libraries required by other software, such as `curl`, `git`, `python3-pip`, `htop`, and `gnupg`.
    *   Cleans up potentially conflicting repository files for VS Code to ensure a clean installation.

3.  **Install Ansible-related Tools (`_install_ansible_tools.yml`)**
    *   Installs `ansible-lint` and `yamllint` using `pip` to help with Ansible content development and quality checks.

4.  **Install Docker (`_install_docker.yml`)**
    *   Adds the official Docker GPG key and repository.
    *   Installs Docker Engine, Docker CLI, Containerd, and Docker Compose.
    *   Adds the current user to the `docker` group to allow running Docker commands without `sudo`. **Note:** The user will need to log out and log back in for this change to take effect.

5.  **Install VirtualBox (`_install_virtualbox.yml`)**
    *   Adds the Oracle VirtualBox GPG key and repository.
    *   Installs the latest stable version of VirtualBox (`virtualbox-7.0`).

6.  **Install Vagrant (`_install_vagrant.yml`)**
    *   Adds the HashiCorp GPG key and repository.
    *   Installs Vagrant.

7.  **Install Visual Studio Code (`_install_vscode.yml`)**
    *   Adds the Microsoft GPG key and repository.
    *   Installs Visual Studio Code.

## Role Variables

This role does not require any specific variables to be set by the user. It is designed to work out-of-the-box.

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
