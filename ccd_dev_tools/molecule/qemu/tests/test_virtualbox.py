# # molecule/qemu/tests/test_virtualbox.py

# import pytest

# # --- Test Case 1: Repository and GPG Key Verification ---


# def test_virtualbox_gpg_key_properties(host):
#     """
#     Test Cases 1.1 & 1.2: Verify VirtualBox GPG key exists, is not empty, and owned by root.
#     """
#     gpg_key = host.file("/etc/apt/keyrings/oracle-virtualbox-2016.gpg")
#     assert gpg_key.exists, "VirtualBox GPG key should exist"
#     assert gpg_key.is_file, "VirtualBox GPG key should be a file"
#     assert gpg_key.user == "root", "VirtualBox GPG key should be owned by root"
#     assert gpg_key.size > 0, "VirtualBox GPG key file should not be empty"


# def test_virtualbox_apt_repository_configured(host):
#     """
#     Test Cases 1.3 & 1.4: Verify VirtualBox apt repository file exists and has correct content.
#     """
#     repo_file = host.file("/etc/apt/sources.list.d/virtualbox.list")
#     assert repo_file.exists, "VirtualBox apt repository file should exist"
#     assert repo_file.is_file, "VirtualBox apt repository file should be a file"
#     # Check that the repo URL is present and points to the GPG key
#     assert repo_file.contains("https://download.virtualbox.org/virtualbox/debian")
#     # Use `grep -F` to treat the string literally and avoid regex issues with `[`
#     assert host.run("grep -F '[signed-by=/etc/apt/keyrings/oracle-virtualbox-2016.gpg]' /etc/apt/sources.list.d/virtualbox.list").rc == 0


# # --- Test Case 2: Package Installation Verification ---


# def test_virtualbox_package_is_installed(host):
#     """
#     Test Case 2.1: Verify that the virtualbox-7.0 package is installed.
#     """
#     pkg = host.package("virtualbox-7.0")
#     assert pkg.is_installed, "Package 'virtualbox-7.0' should be installed"


# # --- Test Case 3: Command and Kernel Module Verification ---


# def test_vboxmanage_command_is_functional(host):
#     """
#     Test Cases 3.1 & 3.2: Verify VBoxManage command is available and functional.
#     """
#     assert host.find_command("VBoxManage"), "'VBoxManage' should be in PATH"
#     cmd = host.run("VBoxManage --version")
#     assert cmd.rc == 0, "'VBoxManage --version' should run successfully"
#     assert "7.0" in cmd.stdout, "VBoxManage should report version 7.0"