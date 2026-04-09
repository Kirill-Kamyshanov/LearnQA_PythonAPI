import requests

url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'

# 1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
response1 = requests.get(url)
print(response1.text)  # Wrong method provided

# 2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
response2 = requests.patch(url)
print(response2.text)  # Wrong HTTP method

# 3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
response3 = requests.get(url, params={"method": "GET"})
print(response3.text)  # {"success":"!"}

# 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
# Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’
# и так далее. И так для всех типов запроса.
# Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра,
# но сервер отвечает так, словно все ок.
# Или же наоборот, когда типы совпадают, но сервер считает, что это не так.

# я сделал один список вместо двух, т.к. значения в них одинаковые
valid_values = ['GET', 'POST', 'PUT', 'DELETE']
success_response = '{"success":"!"}'
failure_response = 'Wrong method provided'


def check_response_text(method, http_type, response):
    """Функция для проверки тела ответа на наличие ошибок"""
    if method == http_type and response == failure_response:
        print(f'Некорректный ответ с method: {method} и http_type: {http_type}')
    if method != http_type and response == success_response:
        print(f'Некорректный ответ с method: {method} и http_type: {http_type}')


# Словарь создан для того чтобы не прописывать ниже вызов для каждого типа запросов
request_function = {
    'GET': requests.get,
    'POST': requests.post,
    'PUT': requests.put,
    'DELETE': requests.delete
}

for http_type in valid_values:
    for method in valid_values:
        # для типа запроса GET отдельная ветвь, т.к. тут уникальный атрибут "params"
        if http_type == 'GET':
            response = request_function[http_type](url, params={'method': method}).text
        else:
            response = request_function[http_type](url, data={'method': method}).text

        check_response_text(method, http_type, response)
