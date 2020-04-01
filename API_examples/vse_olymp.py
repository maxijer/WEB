import requests

dost = requests.get("http://6231f063.ngrok.io/api/vse_olymp").json()
z = dost['all_zadach']
vse = ['image', 'information', 'nazv', 'predmet', 'ssilka']
for i in range(len(z)):
    print(f'image: {z[i][vse[0]]}')
    print(f'information: {z[i][vse[1]]}')
    print(f'nazv: {z[i][vse[2]]}')
    print(f'predmet: {z[i][vse[3]]}')
    print(f'ssilka: {z[i][vse[4]]}')
    print('____________________________')
