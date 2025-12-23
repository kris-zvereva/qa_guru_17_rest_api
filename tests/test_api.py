import requests
from jsonschema import validate

from data.schema import (user_list_schema,
                         error_schema,
                         register_user_schema,
                         update_user_schema,
                         single_user_schema, post_users, put_users)
from data.user_data import (fake_data_user,
                            VALID_USER_EMAIL,
                            VALID_USER_PASSWORD,
                            EXISTING_USER_ID,
                            NON_EXISTENT_USER_ID)



def test_register_user(base_url, headers):
    response = requests.post(url=f'{base_url}/register',
                             headers=headers,
                             json={"email": VALID_USER_EMAIL, "password": VALID_USER_PASSWORD})
    body = response.json()
    assert response.status_code == 200
    validate(body, register_user_schema)

def test_register_user_no_password(base_url, headers):
    response = requests.post(url=f'{base_url}/register',
                             headers=headers,
                             json={"email": "eve.holt@reqres.in"})
    body = response.json()

    assert response.status_code == 400
    assert body['error'] == 'Missing password'
    validate(body, error_schema)

def test_register_user_no_email(base_url, headers):
    response = requests.post(url=f'{base_url}/register',
                             headers=headers,
                             json={"password": "pistol"})
    body = response.json()

    assert response.status_code == 400
    assert body['error'] == 'Missing email or username'
    validate(body, error_schema)

def test_get_user_list(base_url, headers):
    response = requests.get(url=f'{base_url}/users',
                            headers=headers)
    body = response.json()
    assert response.status_code == 200
    assert 'data' in body
    assert len(body['data']) > 0
    validate(body, user_list_schema)

def test_delete_user(base_url, headers):
    response = requests.delete(url=f'{base_url}/users/{EXISTING_USER_ID}',
                               headers=headers)
    assert response.status_code == 204
    assert response.text == ''

def test_update_user(base_url, headers):
    update_data = {
        "name": "morpheus",
        "job": "chiller"
    }
    validate(update_data, put_users)
    response = requests.put(url=f'{base_url}/users/{EXISTING_USER_ID}',
                            headers=headers,
                            json=update_data)
    body = response.json()

    assert response.status_code == 200
    assert 'updatedAt' in body
    assert body['name'] == update_data['name']
    assert body['job'] == update_data['job']
    validate(body, update_user_schema)

def test_get_single_user(base_url, headers):
    response = requests.get(url=f'{base_url}/users/{EXISTING_USER_ID}',
                            headers=headers)
    body = response.json()
    assert response.status_code == 200
    validate(body, single_user_schema)

def test_get_nonexistent_user_returns_404(base_url, headers):
    response = requests.get(url=f'{base_url}/users/{NON_EXISTENT_USER_ID}',
                            headers=headers)

    assert response.status_code == 404


def test_create_user(base_url, headers):
    new_user = fake_data_user()
    json_data = new_user.as_dict()
    validate(json_data, post_users)
    response = requests.post(url=f'{base_url}/users',
                             headers=headers,
                             json=json_data)
    body = response.json()

    assert response.status_code == 201
    assert 'id' in body
    assert 'createdAt' in body

def test_user_list_contains_valid_email_format(base_url, headers):
    response = requests.get(url=f'{base_url}/users',
                            headers=headers)
    body = response.json()

    assert response.status_code == 200
    for user in body['data']:
        assert '@' in user['email']
        assert user['email'].endswith('@reqres.in')

