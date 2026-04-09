import requests
import time

url = 'https://playground.learnqa.ru/ajax/api/longtime_job'

# 1) Создание задачи
response = requests.get(url)
token = response.json().get('token')
seconds = response.json().get('seconds')
params = {"token": token}
print('Task has been created')

# 2) Отправка одного запроса с token ДО того, как задача готова, убеждаемся в правильности поля status
response = requests.get(url, params=params)
if response.json() != {'status': 'Job is NOT ready'}:
    print('Incorrect response before task is ready')
else:
    print('Correct response before task is ready')

# 3) Ожидание нужного количество секунд
print(f'Waiting {seconds} seconds...')
time.sleep(seconds)

# 4) Отправка одного запроса c token ПОСЛЕ того, как задача готова, убеждаемся в правильности поля status и наличии поля result
response = requests.get(url, params=params)
response_body = response.json()
has_error = False
if "result" not in response_body:
    print('Missed "result" field after task is ready')
    has_error = True
if response_body['status'] != 'Job is ready':
    print('Incorrect "status" field after task is ready')
    has_error = True
if not has_error:
    print('Correct response after task is ready')
