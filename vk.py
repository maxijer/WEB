import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import requests


def check_zad(otv, predm):
    dost = requests.get(f"http://6231f063.ngrok.io/api/zadachi_{predm}").json()
    z = dost['all_zadach']
    for i in range(len(z)):
        if z[i]['about'].lower() == ' '.join(otv[4:-2]):
            return z[i]['otvet']


def main():
    vk_session = vk_api.VkApi(
        token='')
    longpoll = VkBotLongPoll(vk_session, '193846592')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            ot = ''
            if 'покажи ответ на задачу' in str(event.obj.message).lower():
                otv = str(event.obj.message['text']).lower().split()
                if otv[-1] == 'физике':
                    ot = check_zad(otv, 'fiz')
                elif otv[-1] == 'математике':
                    ot = check_zad(otv, 'math')
                elif otv[-1] == 'информатике':
                    ot = check_zad(otv, 'inform')
                else:
                    ot = 'Вы где-то допустили ошибку , проверьте ещё раз'
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"{ot}",
                                 random_id=random.randint(0, 2 ** 64))
            elif 'помоги мне' ==  str(event.obj.message['text']).lower():
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Я могу показывать ответ на задачу для этого нужно написать:"
                                         f"покажи ответ на задачу задача по предмет",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
