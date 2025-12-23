import allure
from jsonschema import validate
from utils.api_helper import api_request

from data.schema import (
    user_list_schema,
    error_schema,
    register_user_schema,
    update_user_schema,
    single_user_schema,
    post_users,
    put_users, register_user_request_schema
)
from data.user_data import (
    fake_data_user,
    VALID_USER_EMAIL,
    VALID_USER_PASSWORD,
    EXISTING_USER_ID,
    NON_EXISTENT_USER_ID
)


@allure.epic('ReqRes API Testing')
@allure.feature('User Registration')
class TestUserRegistration:

    @allure.title('Successfully register user with valid credentials')
    @allure.description('Verify that a user can register successfully with valid email and password')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag('smoke', 'registration', 'positive')
    def test_register_user(self, base_url, headers):
        with allure.step(f'Prepare registration data with email={VALID_USER_EMAIL}'):
            request_data = {
                "email": VALID_USER_EMAIL,
                "password": VALID_USER_PASSWORD
            }

        with allure.step('Validate request data schema'):
            validate(request_data, register_user_request_schema)

        with allure.step('Send POST request to /register endpoint'):
            response = api_request(
                'POST',
                f'{base_url}/register',
                headers=headers,
                json=request_data
            )
            body = response.json()

        with allure.step('Verify response'):
            with allure.step('Verify status code is 200 OK'):
                assert response.status_code == 200

            with allure.step('Verify response contains token'):
                assert 'token' in body
                assert body['token']

            with allure.step('Verify response contains ID'):
                assert 'id' in body

            with allure.step('Validate response schema'):
                validate(body, register_user_schema)

    @allure.title('Registration without password returns 400 error')
    @allure.description('Verify that registration without password returns appropriate error')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag('regression', 'registration', 'negative')
    def test_register_user_missing_password(self, base_url, headers):
        with allure.step('Prepare registration data without password'):
            request_data = {"email": "eve.holt@reqres.in"}

        with allure.step('Send POST request to /register without password'):
            response = api_request(
                'POST',
                f'{base_url}/register',
                headers=headers,
                json=request_data
            )
            body = response.json()

        with allure.step('Verify response'):
            with allure.step('Verify status code is 400 Bad Request'):
                assert response.status_code == 400

            with allure.step('Verify error message is "Missing password"'):
                assert body['error'] == 'Missing password'

            with allure.step('Validate error response schema'):
                validate(body, error_schema)

    @allure.title('Registration without email returns 400 error')
    @allure.description('Verify that registration without email returns appropriate error')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag('regression', 'registration', 'negative')
    def test_register_user_missing_email(self, base_url, headers):
        with allure.step('Prepare registration data without email'):
            request_data = {"password": "pistol"}

        with allure.step('Send POST request to /register without email'):
            response = api_request(
                'POST',
                f'{base_url}/register',
                headers=headers,
                json=request_data
            )
            body = response.json()

        with allure.step('Verify response'):
            with allure.step('Verify status code is 400 Bad Request'):
                assert response.status_code == 400

            with allure.step('Verify error message'):
                assert body['error'] == 'Missing email or username'

            with allure.step('Validate error response schema'):
                validate(body, error_schema)


@allure.epic('ReqRes API Testing')
@allure.feature('User Management')
class TestUserManagement:

    @allure.title('Retrieve list of users')
    @allure.description('Verify that API returns correct list of users')
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag('smoke', 'get', 'positive')
    def test_get_user_list(self, base_url, headers):
        with allure.step('Send GET request to /users endpoint'):
            response = api_request('GET', f'{base_url}/users', headers=headers)
            body = response.json()

        with allure.step('Verify response'):
            with allure.step('Verify status code is 200 OK'):
                assert response.status_code == 200

            with allure.step('Verify response contains data field'):
                assert 'data' in body

            with allure.step('Verify user list is not empty'):
                users_count = len(body['data'])
                assert users_count > 0

            with allure.step('Validate user list response schema'):
                validate(body, user_list_schema)

    @allure.title('Retrieve single user by ID')
    @allure.description(f'Verify retrieval of user data with ID={EXISTING_USER_ID}')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag('smoke', 'get', 'positive')
    def test_get_single_user(self, base_url, headers):
        with allure.step(f'Send GET request to /users/{EXISTING_USER_ID}'):
            response = api_request(
                'GET',
                f'{base_url}/users/{EXISTING_USER_ID}',
                headers=headers
            )
            body = response.json()

        with allure.step('Verify response'):
            with allure.step('Verify status code is 200 OK'):
                assert response.status_code == 200

            with allure.step('Verify response contains user data'):
                assert 'data' in body
                user_data = body['data']
                assert user_data['id'] == EXISTING_USER_ID

            with allure.step('Validate single user response schema'):
                validate(body, single_user_schema)

    @allure.title('Non-existent user returns 404 error')
    @allure.description('Verify that request for non-existent user returns appropriate error')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag('regression', 'get', 'negative')
    def test_get_nonexistent_user_returns_404(self, base_url, headers):
        with allure.step(f'Send GET request to /users/{NON_EXISTENT_USER_ID} (non-existent ID)'):
            response = api_request(
                'GET',
                f'{base_url}/users/{NON_EXISTENT_USER_ID}',
                headers=headers
            )

        with allure.step('Verify response'):
            with allure.step('Verify status code is 404 Not Found'):
                assert response.status_code == 404

    @allure.title('Create new user with valid data')
    @allure.description('Verify successful user creation with valid data')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag('smoke', 'post', 'positive')
    def test_create_user(self, base_url, headers):
        with allure.step('Generate random user data'):
            new_user = fake_data_user()
            user_dict = new_user.as_dict()

        with allure.step('Validate request data schema'):
            validate(user_dict, post_users)

        with allure.step('Send POST request to /users endpoint'):
            response = api_request(
                'POST',
                f'{base_url}/users',
                headers=headers,
                json=user_dict
            )
            body = response.json()

        with allure.step('Verify response'):
            with allure.step('Verify status code is 201 Created'):
                assert response.status_code == 201

            with allure.step('Verify response contains ID'):
                assert 'id' in body

            with allure.step('Verify response contains creation timestamp'):
                assert 'createdAt' in body

    @allure.title('Update user information')
    @allure.description('Verify successful user data update using PUT method')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag('smoke', 'put', 'positive')
    def test_update_user(self, base_url, headers):
        with allure.step('Prepare update data'):
            update_data = {
                "name": "morpheus",
                "job": "chiller"
            }

        with allure.step('Validate request data schema'):
            validate(update_data, put_users)

        with allure.step(f'Send PUT request to /users/{EXISTING_USER_ID}'):
            response = api_request(
                'PUT',
                f'{base_url}/users/{EXISTING_USER_ID}',
                headers=headers,
                json=update_data
            )
            body = response.json()

        with allure.step('Verify response'):
            with allure.step('Verify status code is 200 OK'):
                assert response.status_code == 200

            with allure.step('Verify response contains update timestamp'):
                assert 'updatedAt' in body

            with allure.step('Verify name was updated'):
                assert body['name'] == update_data['name']

            with allure.step('Verify job was updated'):
                assert body['job'] == update_data['job']

            with allure.step('Validate update response schema'):
                validate(body, update_user_schema)

    @allure.title('Delete user by ID')
    @allure.description('Verify successful user deletion using DELETE method')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag('smoke', 'delete', 'positive')
    def test_delete_user(self, base_url, headers):
        with allure.step(f'Send DELETE request to /users/{EXISTING_USER_ID}'):
            response = api_request(
                'DELETE',
                f'{base_url}/users/{EXISTING_USER_ID}',
                headers=headers
            )

        with allure.step('Verify response'):
            with allure.step('Verify status code is 204 No Content'):
                assert response.status_code == 204

            with allure.step('Verify response body is empty'):
                assert response.text == ''


@allure.epic('ReqRes API Testing')
@allure.feature('Data Validation')
class TestDataValidation:

    @allure.title('Verify email format in user list')
    @allure.description('Verify that all user emails have correct format')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag('regression', 'validation', 'positive')
    def test_user_list_contains_valid_email_format(self, base_url, headers):
        with allure.step('Send GET request to /users endpoint'):
            response = api_request('GET', f'{base_url}/users', headers=headers)
            body = response.json()

        with allure.step('Verify response'):
            with allure.step('Verify status code is 200 OK'):
                assert response.status_code == 200

            with allure.step('Verify all emails have correct format'):
                for user in body['data']:
                    assert '@' in user['email']
                    assert user['email'].endswith('@reqres.in')