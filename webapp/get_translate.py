import requests
import json
from webapp.config import API_KEY, URL_AUT, URL_TRANSLATE


def get_token():
    try:
        headers = {'Authorization': 'Basic ' + API_KEY}
        token = requests.post(URL_AUT, headers=headers)
        token.raise_for_status()
        return token.text
    except(requests.RequestException):
        print('Сетивая ошибка')
        return False


def get_translate(word):
    try:
        headers = {'Authorization': 'Bearer ' + get_token()}
        params = {
            'text': word,
            'srcLang': 1033,
            'dstLang': 1049
        }
        req = requests.get(URL_TRANSLATE, headers=headers, params=params)
        data = req.json()
        try:
            return data['Translation']['Translation']
        except(IndexError, TypeError):
            return False
    except(requests.RequestException):
        return False
