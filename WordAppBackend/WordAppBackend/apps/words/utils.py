import requests

from words.models import BandToWordModel


def get_word_detail(word):
    url = f'https://v2.xxapi.cn/api/englishwords?word={word}'
    response = requests.get(url)
    data = response.json()
    code = data.get('code')
    if code != 200:
        return {'errmsg': data.get('msg')}
    data = data.get('data')
    del data['bookId']
    del data['word']
    return data


if __name__ == '__main__':
    print(get_word_detail('translate'))
