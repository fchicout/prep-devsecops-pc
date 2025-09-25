# molecule/qemu/tests/test_allure.py

import pytest

# --- Test Case 1: Dependency Verification (Java) ---


def test_java_package_is_installed(host):
    """
    Tests that the 'default-jdk' package is installed.
    """
    pkg = host.package("default-jdk")
    assert pkg.is_installed, "Package 'default-jdk' should be installed"


def test_java_command_is_functional(host):
    """
    Tests that the 'java' command is available and functional.
    """
    assert host.find_command("java"), "'java' command should be in PATH"
    # The 'java -version' command outputs to stderr
    cmd = host.run("java -version")
    assert cmd.rc == 0, "'java -version' should run successfully"
    assert "openjdk" in cmd.stderr.lower()


# --- Test Case 2: Allure Installation and Command Verification ---


def test_allure_package_is_installed(host):
    """
    Tests that the 'allure' package from the .deb file is installed.
    """
    pkg = host.package("allure")
    assert pkg.is_installed, "Package 'allure' should be installed"


def test_allure_command_is_functional(host):
    """
    Tests that the 'allure' command is available and functional.
    """
    assert host.find_command("allure"), "'allure' command should be in PATH"
    cmd = host.run("allure --version")
    assert cmd.rc == 0, "'allure --version' should run successfully"
    assert "2.25.0" in cmd.stdout, "Allure version should be 2.25.0"