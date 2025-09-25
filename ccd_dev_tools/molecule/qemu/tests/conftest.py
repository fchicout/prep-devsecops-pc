# molecule/qemu/tests/conftest.py

import os
import pytest
import testinfra.utils.ansible_runner


@pytest.fixture(scope="session")
def host(request):
    """
    Pytest fixture to initialize the testinfra backend.
    """
    return testinfra.utils.ansible_runner.AnsibleRunner(
        os.environ['MOLECULE_INVENTORY_FILE']).get_host('all')