from http import HTTPStatus

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_read_root_deve_retornar_ok_e_ola_mundo():
    response = client.get('/')  # ACT

    assert response.status_code == HTTPStatus.OK  # ASSERT
    assert response.json() == {'message': 'ola mundo'}
