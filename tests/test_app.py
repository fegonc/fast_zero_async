from http import HTTPStatus


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
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'email': 'teste@test.com',
                'username': 'Teste',
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'email': 'alomae@test.com',
            'username': 'Gmail',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'email': 'alomae@test.com',
        'username': 'Gmail',
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


def test_delete_user(client):
    response = client.delete(
        '/users/1',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'email': 'alomae@test.com',
        'username': 'Gmail',
        'id': 1,
    }


def test_delete_user_not_found(client):
    response = client.delete(
        '/users/1',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
