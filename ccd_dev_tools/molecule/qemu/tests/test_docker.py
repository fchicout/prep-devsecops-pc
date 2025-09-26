# molecule/qemu/tests/test_docker.py

import pytest

# --- Test Case 1: Repository and GPG Key Verification ---


def test_docker_gpg_key_properties(host):
    """
    Test Cases 1.1 & 1.2: Verify Docker GPG key exists, is not empty, and owned by root.
    """
    gpg_key = host.file("/etc/apt/keyrings/docker.gpg")
    assert gpg_key.exists, "Docker GPG key should exist"
    assert gpg_key.is_file, "Docker GPG key should be a file"
    assert gpg_key.user == "root", "Docker GPG key should be owned by root"
    assert gpg_key.size > 0, "Docker GPG key file should not be empty"


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
    Test Case 2: Verify that all required Docker packages are installed.
    This corresponds to test plan items 2.1 through 2.4.
    """
    pkg = host.package(pkg_name)
    assert pkg.is_installed, f"Package '{pkg_name}' should be installed"

# --- Test Case 3: Service and Command Verification ---

def test_docker_service_is_running_and_enabled(host):
    """
    Test Case 3: Verify the Docker service is running and enabled on boot.
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
    Test Case 4: Verify core Docker commands are available and functional.
    This corresponds to test plan items 3.3, 3.4, and 3.5.
    """
    assert host.find_command(command.split()[0]), f"'{command}' should be in PATH"
    cmd = host.run(f"{command} {version_arg}")
    assert cmd.rc == 0, f"'{command} {version_arg}' should run successfully"

def test_docker_daemon_is_accessible(host):
    """
    Test Case 5: Verify the CLI can communicate with the Docker daemon.
    This corresponds to test plan item 3.6.
    """
    # Use sudo to ensure the command has permissions to access the Docker socket.
    cmd = host.run("sudo docker info")
    assert cmd.rc == 0, "'sudo docker info' should run successfully"
    assert "Server Version" in cmd.stdout

# --- Test Case 6: User and Group Verification ---

def test_docker_group_and_socket_permissions(host):
    """
    Test Case 6: Verify the 'docker' group exists and owns the Docker socket.
    This corresponds to test plan items 4.1 and 4.3.
    """
    assert host.group("docker").exists, "The 'docker' group should exist"

    docker_socket = host.file("/var/run/docker.sock")
    assert docker_socket.exists, "Docker socket should exist"
    assert docker_socket.group == "docker", "Docker socket should be owned by 'docker' group"