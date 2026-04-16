from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):

    def test_delete_user_with_id_equals_2(self):
        """Попытка удалить пользователя по ID 2"""
        # AUTH
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id = self.get_json_value(response1, 'user_id')

        # DELETE
        response = MyRequests.delete(f'/user/{user_id}', data=data,
                                     headers={'x-csrf-token': token},
                                     cookies={'auth_sid': auth_sid},
                                     )
        Assertions.assert_code_status(response, 400)
        # сломал тест для настройки репортера
        assert response.json() == {'1111111111error': 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'}, \
            f'Invalid response body: {response.json()}'


    def test_delete_user_successfully(self):
        """Позитивный сценарий удаления пользователя: создание, авторизация, удаление, проверка удаления"""
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

        Assertions.assert_code_status(response, 200)

        # DELETE
        response2 = MyRequests.delete(f'/user/{user_id}',
                                      data=login_data,
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid}
                                      )
        Assertions.assert_code_status(response2, 200)
        # Здесь юзер успешно удаляется (и после проверка даёт код 404. Но тело ответа {'success': '!'} явно не ожидаемое
        assert response2.json() == {"success": f"user {user_id} was deleted"}, f'Unexpected response body: {response2.json()}'

        # CHECK DELETION
        response3 = MyRequests.get(f'/user/{user_id}',
                                 headers = {'x-csrf-token': token},
                                 cookies = {'auth_sid': auth_sid}
                                   )

        Assertions.assert_code_status(response3, 404)


    def test_delete_user_by_another_user(self):
        """Попытка удалить пользователя, будучи авторизованным другим пользователем"""
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

        # DELETE
        another_user_id = int(first_user_id) - 1
        response2 = MyRequests.delete(f'/user/{another_user_id}',
                                      data=login_data,
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid}
                                      )
        Assertions.assert_code_status(response2, 400)
        # Здесь тест падает с некорректным кодом, так что ожидаемое тело ответа я не знаю. Написал как оно могло бы выглядеть
        assert response2.json() == {'error': 'Attempt to delete another user'}, f'Invalid response body: {response2.json()}'



