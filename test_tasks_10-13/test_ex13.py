import pytest
import requests

user_agents = [
    ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
     {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}),

    ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
     {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}),

    ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
     {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}),

    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
     {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}),

    ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
     {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'})
]

wrong_user_agents = {}


@pytest.fixture(scope="session", autouse=True)
def print_wrong_user_agents():
    yield
    print(f'\nИтоговый словарь: {wrong_user_agents}')


def add_wrong_user_agent(user_agent, value):
    if user_agent not in wrong_user_agents:
        wrong_user_agents[user_agent] = [value]
    else:
        wrong_user_agents[user_agent].append(value)


@pytest.mark.parametrize("user_agent, expected_result", user_agents)
def test_user_agent(user_agent, expected_result):
    response = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check",
                            headers={"User-Agent": user_agent})

    resp_body = response.json()
    assert response.status_code == 200, "Wrong response code"
    assert resp_body is not None, "Response body is None"

    data = [("platform", expected_result["platform"]),
            ("browser", expected_result["browser"]),
            ("device", expected_result["device"])]

    for item in data:
        field, expected_value = item
        if resp_body[field] != expected_value:
            add_wrong_user_agent(user_agent, field)
        assert resp_body[field] == expected_value, f"{field} is incorrect"
        assert field in resp_body, f'Missing field {field} in response.json'
