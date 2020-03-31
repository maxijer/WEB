import requests

dost = requests.get("http://127.0.0.1:8080/api/zadachi_fiz").json()
z = dost['all_zadach']
vse = ['about', 'zadacha', 'predmet', 'image']
for i in range(len(z)):
    print(f'about: {z[i][vse[0]]}')
    print(f'zadacha: {z[i][vse[1]]}')
    print(f'predmet: {z[i][vse[2]]}')
    print(f'image: {z[i][vse[3]]}')
    print('____________________________')

