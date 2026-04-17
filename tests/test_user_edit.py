import random
import string

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post('/user/login', data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")


        # EDIT
        new_name = 'Changed Name'
        response3 = MyRequests.put(f'/user/{user_id}',
                                  headers={'x-csrf-token': token},
                                  cookies={'auth_sid': auth_sid},
                                  data={'firstName': new_name}
                                  )

        Assertions.assert_code_status(response3, 200)


        # GET
        response4 = MyRequests.get(f'/user/{user_id}',
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid}
                                 )
        Assertions.assert_json_value_by_name(response4,
                                             'firstName',
                                             new_name,
                                             'Wrong name of the user after edit'
                                             )



    def test_edit_just_created_user_without_authorization(self):
        """Попытка изменить данные пользователя без авторизации"""
        # REGISTER
        user_data = self.create_test_user()
        user_id = user_data.get('user_id')

        # EDIT
        new_name = 'Changed Name'
        response2 = MyRequests.put(f'/user/{user_id}',
                                   data={'firstName': new_name}
                                   )

        Assertions.assert_code_status(response2, 400)
        Assertions.check_response_body(response=response2, expected_response_body={'error': 'Auth token not supplied'})



    def test_edit_created_user_with_different_authorization(self):
        """Попытка изменить данные пользователя, будучи авторизованными другим пользователем"""
        # REGISTER
        user_data = self.create_test_user()
        first_user_id = user_data.get('user_id')
        email = user_data['email']
        password = user_data['password']


        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response = MyRequests.post('/user/login', data=login_data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")


        # EDIT
        new_name = 'Changed Name'
        another_user_id = int(first_user_id) - 1
        response2 = MyRequests.put(f'/user/{another_user_id}',
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'firstName': new_name}
                                   )

        Assertions.assert_code_status(response2, 400)
        # Ожидаемое тело ответа я не знаю, так как этот тест падает. Я могу авторизоваться одним юзером и изменить данные другого
        # Текст ниже добавил для примера каким он мог бы быть
        Assertions.check_response_body(response=response2, expected_response_body={'error': 'Attempt to edit another user`s data '})






    def test_edit_created_user_with_invalid_email(self):
        """Попытка изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @"""
        # REGISTER
        user_data = self.create_test_user()
        user_id = user_data.get('user_id')
        email = user_data['email']
        password = user_data['password']


        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response = MyRequests.post('/user/login', data=login_data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")


        # EDIT
        new_email = email.replace("@", "")
        response2 = MyRequests.put(f'/user/{user_id}',
                                  headers={'x-csrf-token': token},
                                  cookies={'auth_sid': auth_sid},
                                  data={'email': new_email}
                                  )

        Assertions.assert_code_status(response2, 400)
        Assertions.check_response_body(response=response2, expected_response_body={'error': 'Invalid email format'})



    def test_edit_created_user_with_invalid_short_firstname(self):
        """Попытка изменить firstName пользователя, будучи авторизованными тем же пользователем,
        на очень короткое значение в один символ"""
        # REGISTER
        user_data = self.create_test_user()
        user_id = user_data.get('user_id')
        email = user_data['email']
        password = user_data['password']

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response = MyRequests.post('/user/login', data=login_data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")

        # EDIT
        short_first_name = random.choice(string.ascii_uppercase)

        response2 = MyRequests.put(f'/user/{user_id}',
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'first_name': short_first_name}
                                   )

        Assertions.assert_code_status(response2, 400)
        Assertions.check_response_body(response=response2, expected_response_body={'error': 'No data to update'})