import requests


def test_header():
    response = requests.get("https://playground.learnqa.ru/api/homework_header")
    homework_header = response.headers.get("x-secret-homework-header")
    assert homework_header is not None, "Homework header is None"
    assert homework_header == "Some secret value", f"Wrong value of homework_header: {homework_header}"
