import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect', allow_redirects=True)
print(f'Итоговый URL: {response.url}')
print(f'Количество редиректов: {len(response.history)}')
