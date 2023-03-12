# setting.py
TOKEN = '5362155984:AAF74hdjMFPWDkzkCmv-Cg-u2mrF-DGKbUk'  # Токен вашего бота

# Названия каналов и групп, на подписку на которые можно получить extremecoins
channels = ['channel1', 'channel2', 'channel3']  # список названий каналов
groups = ['group1', 'group2', 'group3']  # список названий групп

# Количество extremecoins, которые пользователь получает за подписку на канал или группу
coins_per_channel = 10  # количество extremecoins за подписку на канал
coins_per_group = 20  # количество extremecoins за подписку на группу

# Количество extremecoins, которые пользователь получает за приглашение новых пользователей
coins_per_invite = 50  # количество extremecoins за приглашение нового пользователя

# Количество extremecoins, которые пользователь получает за выполнение других заданий
coins_per_task = 30  # количество extremecoins за выполнение задания (например, оставить комментарий)

# Количество extremecoins, которые пользователь теряет за отписку от канала или группы
coins_for_unsubscribe = coins_per_channel * 2  # количество extremecoins за отписку
