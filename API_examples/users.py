import requests

dost = requests.get("http://6231f063.ngrok.io/api/users").json()
z = dost['all_zadach']
vse = ['surname', 'name', 'age', 'email', 'hashed_password']
for i in range(len(z)):
    print(f'surname: {z[i][vse[0]]}')
    print(f'name: {z[i][vse[1]]}')
    print(f'age: {z[i][vse[2]]}')
    print(f'emai: {z[i][vse[3]]}')
    print(f'hashed_password: {z[i][vse[4]]}')
    print('____________________________')
