from http import HTTPStatus

from src.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'password': '1234',
            'email': 'teste@test.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'teste@test.com',
        'username': 'Teste',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'email': 'alomae@test.com',
            'username': 'Teste',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'email': 'alomae@test.com',
        'username': 'Teste',
        'id': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/0',
        json={
            'email': 'alomae@test.com',
            'username': 'Gmail',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user):
    response = client.delete(
        '/users/1',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}


def test_update_integrity_error(client, user):
    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'password': '1234',
            'email': 'faustoe@test.com',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'email': 'fausto@test.com',
            'username': 'fausto',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Username ou email ja cadastrado'
    }

# def test_delete_user_not_found(client):
#     response = client.delete(
#         '/users/1',
#     )

#     assert response.status_code == HTTPStatus.NOT_FOUND
