import requests

dost = requests.get("http://6231f063.ngrok.io/api/news").json()
z = dost['all_zadach']
vse = ['about', 'news', 'image']
for i in range(len(z)):
    print(f'about: {z[i][vse[0]]}')
    print(f'news: {z[i][vse[1]]}')
    print(f'image: {z[i][vse[2]]}')
    print('____________________________')



