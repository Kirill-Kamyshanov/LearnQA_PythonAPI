from requests import Response
import json

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_body = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response  is not in JSON format. Response text is '{response.text}'"

        assert name in response_body, f"Response JSON does not have key 'name'"
        assert response_body[name] == expected_value, error_message