import requests
from bs4 import BeautifulSoup as bs
from app import resize
from data.olymp import Olymp
from data import db_session

r = requests.get("https://olimpiada.ru/article/887pyth")
data = [(50, 68)]
html = bs(r.content, 'lxml')
subject_url_soups = html.find_all('tr')
for j in data:
    if data.index(j) == 0:
        predmt = "Информатика"
    for i in range(j[0], j[1]):
        level = str(subject_url_soups[i]).split('>')[-4][:-3]
        nazv = str(subject_url_soups[i]).split('>')[4][:-3]
        ssilka = str(subject_url_soups[i]).split('>')[3].split('"')[3]
        r = requests.get(ssilka)
        html = bs(r.content, 'lxml')
        one = html.find('tr').find_all('td')
        history = ''
        data = list()
        three = html.find('table', class_="events_for_activity").find_all('td')
        four = html.find_all('div', class_="info block_with_margin_bottom")
        for i in str(four).split('<p'):
            if str(i)[0] == '>':
                for j in i.split('</p>'):
                    history += str(j.split('<')[0][1:])
        try:
            obsh = str(four[0]).split('<')[2][2:]
        except IndexError:
            pass
        file = str(one).split('"')[3]
        count = 1
        spi = ''
        for i in three[4:]:
            z = str(i).split('>')[2]
            if count % 2 == 1:
                z = str(i).split('>')[3].split(('<'))[0]
            else:
                z = str(i).split('>')[2].split(('<'))[0] + ";"
            spi += z + " "
            count += 1
        zagolovok = nazv + ", " + level + " уровень"
        content = history + " " + spi
        if file[0] == '/':
            response = requests.get(f'https://olimpiada.ru{str(file)}')
            nazv = str(file).split('/')[-1]
            db_session.global_init("db/olymp.sqlite")
            session = db_session.create_session()
            nazvanie = f'static/img/{nazv}'
            with open(f'{nazvanie}', 'wb') as file:
                file.write(response.content)
            resize(nazvanie)
            olimpada = Olymp()
            olimpada.nazv = zagolovok
            olimpada.information = content
            olimpada.predmet = predmt
            olimpada.ssilka = ssilka
            olimpada.image = nazv
            session.add(olimpada)
            session.commit()
            print(1)
        else:
            db_session.global_init("db/olymp.sqlite")
            session = db_session.create_session()
            olimpada = Olymp()
            olimpada.nazv = zagolovok
            olimpada.information = content
            olimpada.predmet = predmt
            olimpada.ssilka = ssilka
            session.add(olimpada)
            session.commit()
            print(2)
