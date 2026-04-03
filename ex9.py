import requests

url_for_get_password = 'https://playground.learnqa.ru/ajax/api/get_secret_password_homework'

# Есть метод: https://playground.learnqa.ru/ajax/api/get_secret_password_homework
# Его необходимо вызывать POST-запросом с двумя параметрами: login и password
# Если login указан и существует, метод вернет нам авторизационную cookie с названием auth_cookie и каким-то значением.


# У метода существует защита от перебора. Если верно указано поле login,
# но передан неправильный password, то авторизационная cookie все равно вернется.
# НО с "неправильным" значением, которое на самом деле не позволит создавать авторизованные запросы.
# Только если и login, и password указаны верно, вернется cookie с "правильным" значением.
# Таким образом используя только метод get_secret_password_homework невозможно узнать,
# передали ли мы верный пароль или нет.

url_for_check_password = 'https://playground.learnqa.ru/ajax/api/check_auth_cookie'
# Если вызвать его без cookie с именем auth_cookie или с cookie, у которой выставлено "неправильное" значение,
# метод вернет фразу "You are NOT authorized".
#
# Если значение cookie “правильное”, метод вернет: “You are authorized”
#
# Коллега говорит, что точно помнит свой login - это значение super_admin

# Top 25 most common passwords by year according to SplashData
# пароль выбран из списка: https://en.wikipedia.org/wiki/List_of_the_most_common_passwords
# Искать его нужно среди списка Top 25 most common passwords by year according to SplashData


# Итак, наша задача - написать скрипт и указать в нем login нашего коллеги и все пароли из Википедии в виде списка. Программа должна делать следующее:
# 1. Брать очередной пароль и вместе с логином коллеги вызывать первый метод get_secret_password_homework. В ответ метод будет возвращать авторизационную cookie с именем auth_cookie и каким-то значением.
#
#
# 2. Далее эту cookie мы должна передать во второй метод check_auth_cookie. Если в ответ вернулась фраза "You are NOT authorized", значит пароль неправильный. В этом случае берем следующий пароль и все заново. Если же вернулась другая фраза - нужно, чтобы программа вывела верный пароль и эту фразу.
#
#
# Ответом к задаче должен быть верный пароль и ссылка на коммит со скриптом.