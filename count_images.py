import os

for currency in os.listdir('data/raw/images'):
    count = len(os.listdir(f'data/raw/images/{currency}'))
    print(f'{currency}: {count} images')