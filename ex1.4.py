import requests

response = requests.get('https://playground.learnqa.ru/api/get_text').text
print(response)
