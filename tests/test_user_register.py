import allure
import random
import string
import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic('Registration cases')
class TestUserRegister(BaseCase):

    @allure.description('Create user successfully')
    @allure.feature('Create user')
    def test_create_user_successfully(self):
        """Успешное создание пользователя"""
        data = self.prepare_registration_data()
        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")


    @allure.description('Create user with existing email')
    @allure.feature('Validation creating user')
    def test_create_user_with_existing_email(self):
        """Попытка создать пользователя с уже существующим email"""
        email = 'vikontov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.check_response_body_with_decoding(response=response,
                                                     expected_response_body=f"Users with email '{email}' already exists")




    @allure.description('Create user without "@" symbol')
    @allure.feature('Validation creating user')
    def test_create_user_without_at_symbol(self):
        """Создание пользователя с некорректным email - без символа @"""
        data = self.prepare_registration_data()
        data['email'] = data['email'].replace('@', '')
        response = MyRequests.post('/user/', data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.check_response_body_with_decoding(response=response, expected_response_body='Invalid email format')



    @allure.description('Create user without any necessary field')
    @allure.feature('Validation creating user')
    @pytest.mark.parametrize('field_to_remove', ['firstName', 'lastName', 'email', 'password', 'username'])
    def test_create_user_without_any_necessary_field(self, field_to_remove):
        """Создание пользователя без указания одного из полей"""
        data = self.prepare_registration_data()
        del data[field_to_remove]
        response = MyRequests.post('/user/', data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f'The following required params are missed: {field_to_remove}'


    @allure.description('Create user with too short name')
    @allure.feature('Validation creating user')
    def test_create_user_with_short_name(self):
        """Создание пользователя с очень коротким именем в один символ"""
        data = self.prepare_registration_data()
        data['firstName'] = random.choice(string.ascii_uppercase)
        response = MyRequests.post('/user/', data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.check_response_body_with_decoding(response=response,
                                                     expected_response_body="The value of 'firstName' field is too short")

    @allure.description('Create user with too long name')
    @allure.feature('Validation creating user')
    def test_create_user_with_too_long_name(self):
        """Создание пользователя с очень длинным именем - длиннее 250 символов (с заглавной буквы)"""
        data = self.prepare_registration_data()
        data['firstName'] = random.choice(string.ascii_uppercase) + ''.join(
            random.choices(string.ascii_lowercase, k=250))
        response = MyRequests.post('/user/', data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.check_response_body_with_decoding(response=response,
                                                     expected_response_body="The value of 'firstName' field is too long")