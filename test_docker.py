# molecule/qemu/tests/test_docker.py

import pytest

# --- Test Case 1: Repository and GPG Key Verification ---


def test_docker_gpg_key_properties(host):
    """
    Test Case 1: Verify Docker GPG key exists and has correct properties.
    This corresponds to test plan items 1.1 and 1.2.
    """
    gpg_key = host.file("/etc/apt/keyrings/docker.gpg")
    assert gpg_key.exists, "Docker GPG key should exist"
    assert gpg_key.is_file, "Docker GPG key should be a file"
    assert gpg_key.user == "root", "Docker GPG key should be owned by root"
    assert gpg_key.size > 0, "Docker GPG key file should not be empty"

def test_docker_apt_repository_configured(host):
    """
    Test Case 2: Verify the system's package manager recognizes the Docker repo.
    This corresponds to test plan items 1.3 and 1.4.
    """
    repo_file = host.file("/etc/apt/sources.list.d/docker.list")
    assert repo_file.exists, "Apt repository file should exist"
    
    # Instead of parsing the file, ask the package manager if it recognizes
    # the repository for the 'docker-ce' package. This is a more robust check.
    policy_output = host.run("apt-cache policy docker-ce").stdout
    assert "https://download.docker.com/linux/" in policy_output, \
        "Docker repository URL not found in apt-cache policy for docker-ce"

# --- Test Case 2: Package Installation Verification ---

DOCKER_PACKAGES = [
    "docker-ce",
    "docker-ce-cli",
    "containerd.io",
    "docker-compose-plugin",
]

@pytest.mark.parametrize("pkg_name", DOCKER_PACKAGES)
def test_docker_packages_are_installed(host, pkg_name):
    """
    Test Case 3: Verify that all required Docker packages are installed.
    This corresponds to test plan items 2.1 through 2.4.
    """
    pkg = host.package(pkg_name)
    assert pkg.is_installed, f"Package '{pkg_name}' should be installed"

# --- Test Case 3: Service and Command Verification ---

def test_docker_service_is_running_and_enabled(host):
    """
    Test Case 4: Verify the Docker service is running and enabled on boot.
    This corresponds to test plan items 3.1 and 3.2.
    """
    docker_service = host.service("docker")
    assert docker_service.is_running, "Docker service should be running"
    assert docker_service.is_enabled, "Docker service should be enabled"

@pytest.mark.parametrize("command, version_arg", [
    ("docker", "--version"),
    ("docker compose", "version")
])
def test_docker_commands_are_functional(host, command, version_arg):
    """
    Test Case 5: Verify core Docker commands are available and functional.
    This corresponds to test plan items 3.3, 3.4, and 3.5.
    """
    assert host.find_command(command.split()[0]), f"'{command}' should be in PATH"
    cmd = host.run(f"{command} {version_arg}")
    assert cmd.rc == 0, f"'{command} {version_arg}' should run successfully"

def test_docker_daemon_is_accessible(host):
    """
    Test Case 6: Verify the CLI can communicate with the Docker daemon.
    This corresponds to test plan item 3.6.
    """
    # Use sudo to ensure the command has permissions to access the Docker socket.
    cmd = host.run("sudo docker info")
    assert cmd.rc == 0, "'sudo docker info' should run successfully"
    assert "Server Version" in cmd.stdout

# --- Test Case 4: User and Group Verification ---

def test_docker_group_and_socket_permissions(host):
    """
    Test Case 7: Verify the 'docker' group exists and owns the Docker socket.
    This corresponds to test plan items 4.1 and 4.3.
    """
    assert host.group("docker").exists, "The 'docker' group should exist"

    docker_socket = host.file("/var/run/docker.sock")
    assert docker_socket.exists, "Docker socket should exist"
    assert docker_socket.group == "docker", "Docker socket should be owned by 'docker' group"