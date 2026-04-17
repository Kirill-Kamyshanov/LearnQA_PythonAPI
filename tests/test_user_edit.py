import allure
import random
import string

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic('Edition cases')
class TestUserEdit(BaseCase):

    @allure.description('Edit user successfully')
    @allure.feature('Creation user')
    def test_edit_just_created_user(self):
        # REGISTER
        with allure.step('Register test user'):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, 'id')

            email = register_data['email']
            password = register_data['password']
            user_id = self.get_json_value(response1, 'id')

        # LOGIN
        with allure.step('Login'):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post('/user/login', data=login_data)
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")


        # EDIT
        with allure.step('Edit test user'):
            new_name = 'Changed Name'
            response3 = MyRequests.put(f'/user/{user_id}',
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid},
                                      data={'firstName': new_name}
                                      )

            Assertions.assert_code_status(response3, 200)


        # GET
        with allure.step('Check that name has been changed'):
            response4 = MyRequests.get(f'/user/{user_id}',
                                     headers={'x-csrf-token': token},
                                     cookies={'auth_sid': auth_sid}
                                     )
            Assertions.assert_json_value_by_name(response4,
                                                 'firstName',
                                                 new_name,
                                                 'Wrong name of the user after edit'
                                                 )


    @allure.description('Edit just created user without authorization')
    @allure.feature('Validation to create user')
    def test_edit_just_created_user_without_authorization(self):
        """Попытка изменить данные пользователя без авторизации"""
        # REGISTER
        with allure.step('Register test user'):
            user_data = self.create_test_user()
            user_id = user_data.get('user_id')

        # EDIT
        with allure.step('Edit test user data without authorization'):
            new_name = 'Changed Name'
            response2 = MyRequests.put(f'/user/{user_id}',
                                       data={'firstName': new_name}
                                       )

            Assertions.assert_code_status(response2, 400)
            Assertions.check_response_body(response=response2, expected_response_body={'error': 'Auth token not supplied'})


    @allure.description('Edit just created user with different authorization')
    @allure.feature('Validation to create user')
    def test_edit_created_user_with_different_authorization(self):
        """Попытка изменить данные пользователя, будучи авторизованными другим пользователем"""
        # REGISTER
        with allure.step('Create test user'):
            user_data = self.create_test_user()
            first_user_id = user_data.get('user_id')
            email = user_data['email']
            password = user_data['password']


        # LOGIN
        with allure.step('Login'):
            login_data = {
                'email': email,
                'password': password
            }
            response = MyRequests.post('/user/login', data=login_data)
            auth_sid = self.get_cookie(response, "auth_sid")
            token = self.get_header(response, "x-csrf-token")


        # EDIT
        with allure.step('Trying to edit another test user data'):
            new_name = 'Changed Name'
            another_user_id = int(first_user_id) - 1
            response2 = MyRequests.put(f'/user/{another_user_id}',
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid},
                                       data={'firstName': new_name}
                                       )

            Assertions.assert_code_status(response2, 400)
            Assertions.check_response_body(response=response2,
                                           expected_response_body={'error': 'This user can only edit their own data.'})




    @allure.description('Edit just created user with invalid email')
    @allure.feature('Validation to create user')
    def test_edit_created_user_with_invalid_email(self):
        """Попытка изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @"""
        # REGISTER
        with allure.step('Create test user'):
            user_data = self.create_test_user()
            user_id = user_data.get('user_id')
            email = user_data['email']
            password = user_data['password']


        # LOGIN
        with allure.step('Login'):
            login_data = {
                'email': email,
                'password': password
            }
            response = MyRequests.post('/user/login', data=login_data)
            auth_sid = self.get_cookie(response, "auth_sid")
            token = self.get_header(response, "x-csrf-token")


        # EDIT
        with allure.step('Trying to edit user with invalid email'):
            new_email = email.replace("@", "")
            response2 = MyRequests.put(f'/user/{user_id}',
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid},
                                      data={'email': new_email}
                                      )

            Assertions.assert_code_status(response2, 400)
            Assertions.check_response_body(response=response2, expected_response_body={'error': 'Invalid email format'})


    @allure.description('Edit just created user with invalid short firstname')
    @allure.feature('Validation to create user')
    def test_edit_created_user_with_invalid_short_firstname(self):
        """Попытка изменить firstName пользователя, будучи авторизованными тем же пользователем,
        на очень короткое значение в один символ"""
        # REGISTER
        with allure.step('Create test user'):
            user_data = self.create_test_user()
            user_id = user_data.get('user_id')
            email = user_data['email']
            password = user_data['password']

        # LOGIN
        with allure.step('Login'):
            login_data = {
                'email': email,
                'password': password
            }
            response = MyRequests.post('/user/login', data=login_data)
            auth_sid = self.get_cookie(response, "auth_sid")
            token = self.get_header(response, "x-csrf-token")

        # EDIT
        with allure.step('Trying to edit user with invalid short firstname'):
            short_first_name = random.choice(string.ascii_uppercase)

            response2 = MyRequests.put(f'/user/{user_id}',
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid},
                                       data={'first_name': short_first_name}
                                       )

            Assertions.assert_code_status(response2, 400)
            Assertions.check_response_body(response=response2, expected_response_body={'error': 'No data to update'})