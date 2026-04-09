import requests

def test_cookie():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    cookie = response.cookies.get("HomeWork")
    assert cookie is not None, "Cookie is None"
    assert cookie == "hw_value", f"Wrong cookie: {cookie}"