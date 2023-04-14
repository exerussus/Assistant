import os

folder_path = input("Введите путь к базе данных: ")
remote_url = input("Введите url с git: ")

if not os.path.exists('data'):
    os.makedirs('data')

with open('data/config.py', 'w') as file:
    file.write('# Код конфигурации\n')
    file.write(f'REMOTE_URL = "{remote_url}"\n')
    file.write(f'FOLDER_PATH = "{folder_path}"\n')

