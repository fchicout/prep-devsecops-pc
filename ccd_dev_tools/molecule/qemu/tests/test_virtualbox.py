# molecule/qemu/tests/test_virtualbox.py

import pytest

# --- Test Case 1: Repository and GPG Key Verification ---
def test_virtualbox_gpg_key_properties(host):
    """
    Test Case 1: Verify VirtualBox GPG key exists and has correct properties.
    This corresponds to test plan items 1.1 and 1.2.
    """
    gpg_key = host.file("/etc/apt/keyrings/oracle-virtualbox-2016.gpg")
    assert gpg_key.exists, "VirtualBox GPG key should exist"
    assert gpg_key.is_file, "VirtualBox GPG key should be a file"
    assert gpg_key.user == "root", "VirtualBox GPG key should be owned by root"
    assert gpg_key.size > 0, "VirtualBox GPG key file should not be empty"

# --- Test Case 2: Package Installation Verification ---

def test_virtualbox_package_is_installed(host):
    """
    Test Case 2: Verify that the correct VirtualBox package is installed.
    This corresponds to test plan item 2.1.
    """
    pkg = host.package("virtualbox-7.0")
    assert pkg.is_installed, "Package 'virtualbox-7.0' should be installed"

# --- Test Case 3: Command Verification ---

def test_vboxmanage_command_is_functional(host):
    """
    Test Case 3: Verify the VBoxManage command is available and functional.
    This corresponds to test plan items 3.1 and 3.2.
    """
    assert host.find_command("VBoxManage"), "'VBoxManage' should be in PATH"
    cmd = host.run("VBoxManage --version")
    assert cmd.rc == 0, "'VBoxManage --version' should run successfully"
    assert "7.0" in cmd.stdout, "VBoxManage should report version 7.0"