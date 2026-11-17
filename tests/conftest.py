import pytest
from fastapi.testclient import TestClient

from aluno_api import app as app_module
from aluno_api.app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    app_module.database = []
    app_module._id_counter[0] = 0
    yield
    app_module.database = []
    app_module._id_counter[0] = 0
