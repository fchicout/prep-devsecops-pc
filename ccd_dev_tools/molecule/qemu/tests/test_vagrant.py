# molecule/qemu/tests/test_vagrant.py

import pytest

# --- Test Case 1: Repository and GPG Key Verification ---


def test_hashicorp_gpg_key_properties(host):
    """
    Test Cases 1.1 & 1.2: Verify HashiCorp GPG key exists, is not empty, and owned by root.
    """
    gpg_key = host.file("/etc/apt/keyrings/hashicorp.gpg")
    assert gpg_key.exists, "HashiCorp GPG key should exist"
    assert gpg_key.is_file, "HashiCorp GPG key should be a file"
    assert gpg_key.user == "root", "HashiCorp GPG key should be owned by root"
    assert gpg_key.size > 0, "HashiCorp GPG key file should not be empty"


def test_hashicorp_apt_repository_configured(host):
    """
    Test Cases 1.3 & 1.4: Verify HashiCorp apt repository file exists and has correct content.
    """
    repo_file = host.file("/etc/apt/sources.list.d/hashicorp.list")
    assert repo_file.exists, "HashiCorp apt repository file should exist"
    assert repo_file.is_file, "HashiCorp apt repository file should be a file"
    assert repo_file.contains("https://apt.releases.hashicorp.com")
    assert repo_file.contains("[signed-by=/etc/apt/keyrings/hashicorp.gpg]")


# --- Test Case 2: Package Installation Verification ---

def test_vagrant_package_is_installed(host):
    """
    Test Case 2.1: Verify that the vagrant package is installed.
    """
    pkg = host.package("vagrant")
    assert pkg.is_installed, "Package 'vagrant' should be installed"


# --- Test Case 3: Command Verification ---

def test_vagrant_command_is_functional(host):
    """
    Test Cases 3.1 & 3.2: Verify vagrant command is available and functional.
    """
    assert host.find_command("vagrant"), "'vagrant' command should be in PATH"
    cmd = host.run("vagrant --version")
    assert cmd.rc == 0, "'vagrant --version' should run successfully"
    assert "Vagrant" in cmd.stdout, "Command output should contain 'Vagrant'"