from flask import Flask, request
import json

app = Flask(__name__)
sessionStorage = {}
flag = False


@app.route('/post', methods=['POST'])
# Функция получает тело запроса и возвращает ответ.
# Внутри функции доступен request.json - это JSON,
# который отправила нам Алиса в запросе POST
def main():
    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом при помощи библиотеки json
    # преобразуем в JSON и отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    return json.dumps(response)


def handle_dialog(req, res):
    global flag
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Инстаграм закрыт.",
                "Инстаграм.",
                "Открой инстаграм.",
                "Инстаграм закрыли."

            ]
        }
        res['response']['text'] = 'Привет! Навык запущен.'
        res['response']['buttons'] = get_suggests(user_id)
        return
    if 'конечно' in req['request']['original_utterance'].lower() and flag:
        res['response']['text'] = 'Хорошого пользования!'
        res['response']['end_session'] = True
    elif "а что это?" in req['request']['original_utterance'].lower() and flag:
        res['response']['text'] = f'''Newgram - это новая социальная сеть с привычным и понятным интерфейсом, широкими возможностями и простыми условиями работы.
                                  В Newgram предусмотрены все возможности для общения, бизнеса, ведения блога, публикации новостей или создания собственного проекта.'''
        res['response']['buttons'] = get_suggests(user_id)
    elif "кто это создал?" in req['request']['original_utterance'].lower() and flag:
        res['response'][
            'text'] = 'Эту социальную сеть разработали два программиста из яндекс лицея. Их ники - DTEAA и Nytrock'
        res['response']['buttons'] = get_suggests(user_id)
    if 'инстаграм' in req['request']['original_utterance'].lower():
        if req['request']['original_utterance'].lower() == 'инстаграм закрыт.' or req['request'][
            'original_utterance'].lower() == 'инстаграм закрыли.':
            res['response'][
                'text'] = 'Да, Instargram теперь закрыт. Но появился русский аналог - Newgram. Хочешь перейти на него?'
            flag = True
            res['response']['buttons'] = get_suggests(user_id)
        elif req['request']['original_utterance'].lower() == 'открой инстаграм.':
            res['response'][
                'text'] = 'Instagram теперь заблокирован в России. Но ты можешь попробовать новый аналог - Newgram. ' \
                          'Хочешь перейти на него?'
            flag = True
            res['response']['buttons'] = get_suggests(user_id)
        else:
            res['response']['text'] = 'Instagram больше нет в России. Но теперь есть Newgram. Хочешь перейти на него?'
            flag = True
            res['response']['buttons'] = get_suggests(user_id)
        return


def get_suggests(user_id):
    global flag
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if flag:
        suggests.clear()
        suggests.append({"title": "А что это?", "hide": True})
        suggests.append({"title": "Кто это создал?", "hide": True})
        suggests.append({
            "title": "Конечно",
            "url": "https://vk.com/nytrock",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()
