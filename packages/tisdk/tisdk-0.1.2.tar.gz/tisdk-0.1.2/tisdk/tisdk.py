# coding=utf8

import base64
import sys
import datetime
import hashlib
import hmac
import json
import requests

from tisdk.sm4 import encrypt_ecb, decrypt_ecb

DEFAULT_HOST = 'https://api.taiqiyun.net'


class Ti:
    def __init__(self, username, secret_key, slience=False):
        self.username = username
        self.secret_key = secret_key
        self.slience = slience

    def request(self, method, url, data=None):
        return ti_request(self.username, self.secret_key, method, url, data, self.slience)


def general_hmac(text, key):
    myhmac = hmac.new(key=key.encode('utf8'), digestmod=hashlib.sha256)
    myhmac.update(text.encode('utf8'))
    return base64.b64encode(myhmac.digest()).decode('utf8')


def get_headers(username, secret_key):

    req_time = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    signing_string = 'x-date: %s\nusername: %s' % (req_time, username)
    signature = general_hmac(signing_string, secret_key)

    headers = {
        'x-date': req_time,
        'username': username,
        'signature': signature,
    }
    return headers


def encrypt_body(data, secret_key):
    if data:
        json_body = {'reqdata': encrypt_ecb(json.dumps(data), secret_key)}
    else:
        json_body = None
    return json_body


def decrypt_response(r, secret_key, slience=False):
    assert isinstance(r, requests.Response), r
    try:
        res = r.json()
        if 'data' in res:
            data = res['data']
            data = decrypt_ecb(data, secret_key)
            try:
                data = json.loads(data)
            except Exception as e:
                pass
            res['data'] = data
            
            if 200 <= r.status_code < 400:
                res = data

    except Exception as e:
        if not slience:
            print(e)
        res = r.text

    return res


def ti_request(username, secret_key, method, url, data=None, slience=False):
        
    if 'http' not in url:
        url = DEFAULT_HOST + url

    if not slience:
        print(method.upper(), url)

    headers = get_headers(username, secret_key)

    if not slience:
        print('Request Headers:', headers)

    json_body = encrypt_body(data, secret_key)

    if not slience:
        print('Request Body:', json_body)
        
    r = requests.request(method, url, json=json_body, headers=headers)
    if not slience:
        print('Response:', r.status_code, r.text)

    res = decrypt_response(r, secret_key, slience)

    return res


def main():
    # pip intall tisdk
    # tireq to_9012345678_grs 3292a4f76c0d46bf post http://test.tflag.cn/grs/v1/open_match name:美团

    args = sys.argv

    len_args = len(args)
    if len_args > 4:
        username = args[1]
        secret_key = args[2]
        method = args[3]
        url = args[4]
        data = args[5] if len_args > 5 else None
    else:
        print('Usage: tireq username secret_key method url [foo:bar,foo2:bar2...]')
        sys.exit(1)

    if data:
        items = data.split(',')
        data = {item.split(':')[0]: item.split(':')[1] for item in items}

    res = ti_request(username, secret_key, method, url, data)

    try:
        res = json.dumps(res, ensure_ascii=False, indent=2)
    except Exception as e:
        print(e)
        
    print(res)


if __name__ == '__main__':
    main()


