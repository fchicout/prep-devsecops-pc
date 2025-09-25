# molecule/qemu/tests/test_ansible_tools.py

import pytest

# Define the packages to be tested. This makes it easy to add more later.
ANSIBLE_TOOL_PACKAGES = [
    "ansible-lint",
    "yamllint"
]


@pytest.mark.parametrize("pkg_name", ANSIBLE_TOOL_PACKAGES)
def test_ansible_tool_packages_are_installed(host, pkg_name):
    """
    Test case 1: Verify that the ansible-lint and yamllint packages are installed.
    """
    pkg = host.package(pkg_name)
    assert pkg.is_installed


@pytest.mark.parametrize("command_name", ANSIBLE_TOOL_PACKAGES)
def test_ansible_tool_commands_are_available(host, command_name):
    """
    Test case 2: Verify that the executables are available in the system's PATH.
    """
    assert host.find_command(command_name)


@pytest.mark.parametrize("version_command", [
    "ansible-lint --version",
    "yamllint --version"
])
def test_ansible_tool_commands_are_functional(host, version_command):
    """
    Test case 3: Run a smoke test to ensure the tools are functional.
    """
    cmd = host.run(version_command)
    assert cmd.rc == 0, f"Command '{version_command}' failed with exit code {cmd.rc}"