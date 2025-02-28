import os

file1 = os.path.join(os.getcwd(), 'output', 'accounts.txt')
file2 = os.path.join(os.getcwd(), 'signup_links.txt')

with open(file1, encoding='utf-8') as file:
    text = file.read()

with open(file2, encoding='utf-8') as file:
    lines = file.read().splitlines()

with open(os.path.join(os.getcwd(), 'filtered.txt'), 'a', encoding='utf-8') as file:
    for line in lines:
        email, pwd, link = line.split('|')

        if not email in text:
            file.write(f'{line}\n')
