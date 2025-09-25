# molecule/qemu/tests/test_prereqs.py

import pytest

# --- Test Case 1: Directory Verification ---


def test_keyrings_directory_properties(host):
    """
    Test Cases 1.1-1.4: Verify /etc/apt/keyrings directory properties.
    """
    keyrings_dir = host.file("/etc/apt/keyrings")
    assert keyrings_dir.exists, "Directory /etc/apt/keyrings should exist"
    assert keyrings_dir.is_directory, "/etc/apt/keyrings should be a directory"
    assert keyrings_dir.user == "root", "Owner should be root"
    assert keyrings_dir.group == "root", "Group should be root"
    assert keyrings_dir.mode == 0o755, "Permissions should be 0755"


# --- Test Case 2: Prerequisite Package Installation ---

PREREQ_PACKAGES = [
    "apt-transport-https",
    "ca-certificates",
    "curl",
    "gpg",
    "gnupg",
    "htop",
    "nload",
    "python3-pip",
    "python3-venv",
    "wget",
    "git",
]


@pytest.mark.parametrize("pkg_name", PREREQ_PACKAGES)
def test_prereq_packages_are_installed(host, pkg_name):
    """
    Test Case 2.1: Verify that all prerequisite packages are installed.
    """
    pkg = host.package(pkg_name)
    assert pkg.is_installed, f"Package '{pkg_name}' should be installed"


# --- Test Case 3: Prerequisite Command Availability and Functionality ---

COMMAND_SMOKE_TESTS = {
    "curl": "curl --version",
    "gpg": "gpg --version",
    "htop": "htop --version",
    "nload": "nload --version",
    "pip3": "pip3 --version",
    "wget": "wget --version",
    "git": "git --version",
    "python3-venv": "python3 -m venv --help",
}


@pytest.mark.parametrize("command_name", COMMAND_SMOKE_TESTS.keys())
def test_prereq_commands_are_available(host, command_name):
    """
    Test Cases 3.1-3.8 (Availability): Verify executables are in the PATH.
    """
    assert host.find_command(command_name)


@pytest.mark.parametrize("version_command", COMMAND_SMOKE_TESTS.values())
def test_prereq_commands_are_functional(host, version_command):
    """
    Test Cases 3.1-3.8 (Functionality): Run a smoke test on each command.
    """
    cmd = host.run(version_command)
    assert cmd.rc == 0, f"Command '{version_command}' failed with exit code {cmd.rc}"