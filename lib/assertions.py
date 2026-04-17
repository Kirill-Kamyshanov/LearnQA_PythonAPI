from requests import Response
import json

from lib.error_reporter import ErrorReporter


class Assertions:


    @staticmethod
    def _json_decoding(response):
        """Служебная функция для декодирования ответов в формате JSON"""
        try:
            response_body = response.json()
        except json.decoder.JSONDecodeError:
            ErrorReporter.add_error(step='Декодирование JSON ответа',
                                    waiting_result='Ответ успешно преобразован в JSON объект',
                                    actual_result=f"Ошибка при попытке декодирования. Ответ не в JSON формате:'{response.text}'")
            assert False, f"Response  is not in JSON format. Response text is '{response.text}'"
            return False
        return response_body



    @staticmethod
    def check_response_body_with_decoding(response: Response, expected_response_body):
        """Проверка соответствия фактического тела ответа в unicode ожидаемому"""
        try:
            response_body = response.content.decode('utf-8')
        except UnicodeDecodeError:
            ErrorReporter.add_error(step='Декодирование ответа в utf-8',
                                    waiting_result='Ответ успешно преобразован в кодировку utf-8',
                                    actual_result=f"Ошибка при попытке декодирования:'{response.text}'")
            assert False, f"Error during convertion response. Response text is '{response.text}'"

        if response_body != expected_response_body:
            ErrorReporter.add_error(step='Проверка соответствия фактического тела ответа в unicode ожидаемому',
                                    waiting_result=f'{expected_response_body}',
                                    actual_result=f"{response_body}")
        assert response_body == expected_response_body, f"Incorrect response_body: '{response_body}'"




    @staticmethod
    def check_response_body(response: Response, expected_response_body):
        """Проверка соответствия фактического тела ответа в JSON ожидаемому"""
        response_body = Assertions._json_decoding(response)

        if response_body != expected_response_body:
            ErrorReporter.add_error(step='Проверка соответствия фактического тела ответа JSON ожидаемому',
                                    waiting_result=f"{expected_response_body}",
                                    actual_result=f"{response_body}"
                                    )
        assert response_body == expected_response_body, f'Invalid response body: {response_body}'




    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        """Проверка наличия и значения ключа в JSON объекте"""
        response_body = Assertions._json_decoding(response)

        if name not in response_body:
            ErrorReporter.add_error(step='Проверка наличия ключа в теле ответа',
                                    waiting_result=f"Ключ '{name}' в теле ответа",
                                    actual_result=f"Ключ '{name}' отсутствует в теле ответа"
                                    )
        assert name in response_body, f"Response JSON does not have key '{name}'"

        if response_body[name] != expected_value:
            ErrorReporter.add_error(step=f"Проверка значения ключа {name} в теле ответа",
                                    waiting_result='Значение ключа соответствует ожидаемому',
                                    actual_result=f"Значение ключа не соответствует ожидаемому:'{response_body[name]}'"
                                    )
        assert response_body[name] == expected_value, error_message


    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        """Проверка соответствия фактического статус-кода ожидаемому"""
        if response.status_code != expected_status_code:
            ErrorReporter.add_error(step='Проверка статус-кода',
                                    waiting_result=expected_status_code,
                                    actual_result=response.status_code
                                    )
        assert response.status_code == expected_status_code,\
            f"Unexpected status code.  Expected:{expected_status_code} Actual:{response.status_code}"


    @staticmethod
    def assert_json_has_no_key(response: Response, name):
        """Проверка отсутствия одного ключа в JSON объекте"""
        response_body = Assertions._json_decoding(response)

        if name in response_body:
            ErrorReporter.add_error(step=f"Проверка отсутствия ключа '{name}' в теле ответа",
                                    waiting_result=f"Ключ {name} отсутствует в теле ответа",
                                    actual_result=f"Ключ {name} приходит в теле ответа"
                                    )
        assert name not in response_body, f"Response JSON shouldn't have key {name}. But it's present"


    @staticmethod
    def assert_json_has_no_keys(response: Response, names: list):
        """Проверка отсутствия набора ключей в JSON объекте"""
        response_body = Assertions._json_decoding(response)

        for name in names:
            if name in response_body:
                ErrorReporter.add_error(step=f"Проверка отсутствия ключа '{name}' в теле ответа",
                                        waiting_result=f"Ключ {name} отсутствует в теле ответа",
                                        actual_result=f"Ключ {name} приходит в теле ответа"
                                        )
            assert name not in response_body, f"Response JSON  have key {name}"


    @staticmethod
    def assert_json_has_key(response: Response, name):
        """Проверка наличия одного ключа в JSON объекте"""
        response_body = Assertions._json_decoding(response)

        if name not in response_body:
            ErrorReporter.add_error(step=f"Проверка наличия ключа '{name}' в теле ответа",
                                    waiting_result=f"Ключ {name} приходит в теле ответа",
                                    actual_result=f"Ключ {name} отсутствует в теле ответа"
                                    )
        assert name in response_body, f"Response JSON does not have key {name}"


    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        """Проверка наличия набора ключей в JSON объекте"""
        response_body = Assertions._json_decoding(response)

        for name in names:
            if name not in response_body:
                ErrorReporter.add_error(step=f"Проверка наличия ключа '{name}' в теле ответа",
                                        waiting_result=f"Ключ {name} приходит в теле ответа",
                                        actual_result=f"Ключ {name} отсутствует в теле ответа"
                                        )
            assert name in response_body, f"Response JSON does not have key {name}"
