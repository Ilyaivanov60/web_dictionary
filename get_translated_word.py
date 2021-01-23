import requests
import json
from webapp.config import API_KEY, URL_AUT, URL_TRANSLATE, RULang, ENLang


def get_token():
    try:
        headers = {'Authorization': 'Basic ' + API_KEY}
        token = requests.post(URL_AUT, headers=headers)
        token.raise_for_status()
        return token.text
    except(requests.RequestException):
        print('Сетивая ошибка')
        return False

def get_translation(word):
    try:
        headers = {'Authorization': 'Bearer ' + get_token()}
        params = {
            'text': word,
            'srcLang': ENLang,
            'dstLang': RULang
        }
        req = requests.get(URL_TRANSLATE, headers=headers, params=params)
        data = req.json()
        try:
            return data['Translation']['Translation']
        except(IndexError, TypeError):
            return False
    except(requests.RequestException):
        return False

if __name__ == '__main__':
    print(get_translation('ghlls'))