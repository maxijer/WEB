import requests

dost = requests.get("http://127.0.0.1:8080/api/math").json()
z = dost['all_zadach']
vse = ['image', 'information', 'nazv', 'predmet', 'ssilka']
for i in range(len(z)):
    print(f'image: {z[i][vse[0]]}')
    print(f'information: {z[i][vse[1]]}')
    print(f'nazv: {z[i][vse[2]]}')
    print(f'predmet: {z[i][vse[3]]}')
    print(f'ssilka: {z[i][vse[4]]}')
    print('____________________________')
