# # molecule/qemu/tests/test_docker.py

# import pytest

# # --- Test Case 1: Repository and GPG Key Verification ---


# def test_docker_gpg_key_properties(host):
#     """
#     Test Cases 1.1 & 1.2: Verify Docker GPG key exists, is not empty, and owned by root.
#     """
#     gpg_key = host.file("/etc/apt/keyrings/docker.gpg")
#     assert gpg_key.exists, "Docker GPG key should exist"
#     assert gpg_key.is_file, "Docker GPG key should be a file"
#     assert gpg_key.user == "root", "Docker GPG key should be owned by root"
#     assert gpg_key.size > 0, "Docker GPG key file should not be empty"


# def test_docker_apt_repository_configured(host):
#     """
#     Test Cases 1.3 & 1.4: Verify Docker apt repository file exists and has correct content.
#     """
#     repo_file = host.file("/etc/apt/sources.list.d/docker.list")
#     assert repo_file.exists, "Docker apt repository file should exist"
#     assert repo_file.is_file, "Docker apt repository file should be a file"
#     # Check that the repo URL is present and points to the GPG key
#     # The role uses ansible_distribution_release, which is 'jammy' for the test instance
#     assert repo_file.contains("https://download.docker.com/linux/ubuntu jammy stable")
#     # Use `grep -F` to treat the string literally and avoid regex issues with `[`
#     assert host.run("grep -F '[signed-by=/etc/apt/keyrings/docker.gpg]' /etc/apt/sources.list.d/docker.list").rc == 0


# # --- Test Case 2: Package Installation Verification ---

# DOCKER_PACKAGES = [
#     "docker-ce",
#     "docker-ce-cli",
#     "containerd.io",
#     "docker-compose-plugin",
# ]


# @pytest.mark.parametrize("pkg_name", DOCKER_PACKAGES)
# def test_docker_packages_are_installed(host, pkg_name):
#     """
#     Test Cases 2.1-2.4: Verify that all Docker-related packages are installed.
#     """
#     pkg = host.package(pkg_name)
#     assert pkg.is_installed, f"Package '{pkg_name}' should be installed"


# # --- Test Case 3: Service and Command Verification ---


# def test_docker_service_is_running_and_enabled(host):
#     """
#     Test Cases 3.1 & 3.2: Verify the Docker service is running and enabled.
#     """
#     docker_service = host.service("docker")
#     assert docker_service.is_running, "Docker service should be running"
#     assert docker_service.is_enabled, "Docker service should be enabled"


# @pytest.mark.parametrize("command, version_arg", [
#     ("docker", "--version"),
#     ("docker compose", "version")
# ])
# def test_docker_commands_are_functional(host, command, version_arg):
#     """
#     Test Cases 3.3, 3.4 & 3.5: Verify commands are available and functional.
#     """
#     assert host.find_command(command.split()[0]), f"'{command}' should be in PATH"
#     cmd = host.run(f"{command} {version_arg}")
#     assert cmd.rc == 0, f"'{command} {version_arg}' should run successfully"


# def test_docker_daemon_is_accessible(host):
#     """
#     Test Case 3.6: Verify the CLI can communicate with the Docker daemon.
#     """
#     # Run with sudo to overcome the session permission issue for the vagrant user
#     cmd = host.run("sudo docker info")
#     assert cmd.rc == 0, "'sudo docker info' should run successfully"
#     assert "Server Version" in cmd.stdout


# # --- Test Case 4: User and Group Verification ---


# def test_docker_group_and_socket_permissions(host):
#     """
#     Test Cases 4.1 & 4.3: Verify the 'docker' group exists and owns the socket.
#     """
#     assert host.group("docker").exists, "The 'docker' group should exist"

#     docker_socket = host.file("/var/run/docker.sock")
#     assert docker_socket.exists, "Docker socket should exist"
#     assert docker_socket.group == "docker", "Docker socket should be owned by 'docker' group"