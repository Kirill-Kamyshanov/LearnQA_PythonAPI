import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic('Cases to get user info')
class TestUserGet(BaseCase):

    data = {
        'email': 'vinkotov@example.com',
        'password': '1234'
    }

    @allure.description('Get user details without authorization')
    @allure.feature('Validation to get user data')
    def test_get_user_details_not_auth(self):
        """Получение данных по юзеру без авторизации"""
        with allure.step('Trying to get user details without authorization'):
            response = MyRequests.get('/user/2')
            unexpected_fields = ['email', 'firstName', 'lastName']

            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_key(response, 'username')
            Assertions.assert_json_has_no_keys(response, unexpected_fields)


    @allure.description('Get user details with auth as same user')
    @allure.feature('Get user data')
    def test_get_user_details_auth_as_same_user(self):
        """Авторизация пользователем с последующим получением данных по нему """
        with allure.step('Authorization'):
            response1 = MyRequests.post('/user/login', data=self.data)
            auth_sid = self.get_cookie(response1, 'auth_sid')
            token = self.get_header(response1, 'x-csrf-token')
            user_id_from_auth_method = self.get_json_value(response1, 'user_id')

        with allure.step('Get user data after successful authorization'):
            response2 = MyRequests.get(f'/user/{user_id_from_auth_method}',
                                     headers = {'x-csrf-token': token},
                                     cookies = {'auth_sid': auth_sid})

            expected_fields = ['lastName', 'firstName', 'username', 'email']
            Assertions.assert_code_status(response2, 200)
            Assertions.assert_json_has_keys(response2, expected_fields)


    @allure.description('Get user details with auth as different user')
    @allure.feature('Validation to get user data')
    def test_get_user_details_auth_as_another_user(self):
        """Авторизация одним пользователем и попытка получить данные другого"""
        with allure.step('Authorization'):
            response1 = MyRequests.post('/user/login', data=self.data)
            auth_sid = self.get_cookie(response1, 'auth_sid')
            token = self.get_header(response1, 'x-csrf-token')
            user_id_from_auth_method = self.get_json_value(response1, 'user_id')
            another_user_id = 1 if user_id_from_auth_method != 1 else 2

        with allure.step('Trying to get details another user after authorization'):
            response2 = MyRequests.get(f'/user/{another_user_id}',
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid})

            unexpected_fields = ['lastName', 'firstName', 'id', 'email']

            Assertions.assert_code_status(response2, 200)
            Assertions.assert_json_has_key(response2, 'username')
            Assertions.assert_json_has_no_keys(response2, unexpected_fields)
