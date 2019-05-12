# coding: utf-8


import fanfou
import shelve
import time
import datetime

consumer = {'key': '08cfccfb3096e4b203b2ef266c12f48e', 'secret': '016636d21ac5b7a6bd82fa2f08142deb'}
client = fanfou.XAuth(consumer, 'chriself', '1qaz!QAZ')

fanfou.bound(client)

db = shelve.open('dream.db')

kw_words = ['梦见', '梦到', '梦里', '记梦', '一个梦']
unique_id = '~YJSpl83mJv4'



def work():
    resp_1 = client.statuses.public_timeline()
    resp_2 = client.statuses.public_timeline()
    for item in resp_1.json():
        status_id = item['id']
        if status_id in db.keys():
            continue

        for kwd in kw_words:
            if kwd in item['text']:
                user = item['user']
                if unique_id not in user['unique_id']:
                    id_1 = item['id']
                    db[status_id] = True
                    send(item)
                    break

    for item in resp_2.json():
        status_id = item['id']
        if status_id in db.keys():
            continue

    for kwd in kw_words:
        if kwd in item['text']:
            user = item['user']
            if unique_id not in user['unique_id']:
                id_2 = item['id']
                if id_2 != id_1:
                    db[status_id] = True
                    send(item)
                    break


def send(item):
    status = '#记梦# 转@%s %s' % (item['user']['name'], item['text'])
    body = {'status': status, 'repost_status_id': item['id']}
    try:
        client.statuses.update(body)
        print("one msg found...")
    except:
        pass


if __name__ == '__main__':
    while True:
        print("start over")
        print(datetime.datetime.now())
        try:
            work()
        except:
            pass
        time.sleep(30)
