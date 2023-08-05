# class AesUtil:
#     def __init__(self, key):
#         len_key = len(key)
#         assert len_key in [16, 24, 32], 'the length of SECRET_KEY must be 16 24 or 32'
#         self.key = key
#         self.iv = key
#         self.mode = AES.MODE_CBC
#         self.pad = lambda s: s + (len_key - len(s.encode('utf8')) % len_key) * chr(len_key - len(s.encode('utf8')) % len_key)
#         self.unpad = lambda s: s[0:-ord(s[-1])]
#
#     # 加密函数
#     def encrypt(self, text):
#         cryptor = AES.new(self.key, self.mode, self.iv)
#         self.ciphertext = cryptor.encrypt(self.pad(text))
#         # AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题，使用base64编码
#         return b2a_hex(self.ciphertext).decode('utf8')
#
#     # 解密函数
#     def decrypt(self, text):
#         cryptor = AES.new(self.key, self.mode, self.iv)
#         plain_text = cryptor.decrypt(a2b_hex(text))
#         return self.unpad(plain_text.decode('utf8'))


# def ti_request_aes(username, secret_key, method, url, data=None, slience=False, supertoken=''):
#     if not username and not secret_key and supertoken:
#         data = {
#             'supertoken': supertoken,
#             'url': url,
#         }
#         r = requests.post(SUPERTOKEN_URL, data=data)
#         if r.status_code != 200:
#             print(r.text)
#             return
#         res = r.json()
#         service_name = res['service_name']
#         username = res['username']
#         secret_key = res['secret_key']
#         if not slience:
#             print(service_name, username, secret_key)
#
#     if 'http' not in url:
#         url = DEFAULT_HOST + url
#
#     if not slience:
#         print(method.upper(), url)
#
#     aes_utils = AesUtil(secret_key)
#     req_time = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
#     signing_string = 'x-date: %s\nusername: %s' % (req_time, username)
#     signature = general_hmac(signing_string, secret_key)
#
#     headers = {
#         'X-DATE': req_time,
#         'username': username,
#         'signature': signature,
#     }
#
#     if not slience:
#         print('Request Headers:', headers)
#
#     if data:
#         json_body = {'reqdata': aes_utils.encrypt(json.dumps(data))}
#         if not slience:
#             print('Request Body:', json_body)
#     else:
#         json_body = None
#
#     r = requests.request(method, url, json=json_body, headers=headers)
#     if not slience:
#         print('Response:', r.status_code, r.text)
#
#     try:
#         res = r.json()
#         if 'data' in res:
#             data = res['data']
#             data = aes_utils.decrypt(data)
#             try:
#                 data = json.loads(data)
#             except Exception as e:
#                 pass
#             res['data'] = data
#
#             if 200 <= r.status_code < 400:
#                 res = data
#
#     except Exception as e:
#         if not slience:
#             print(e)
#         res = r.text
#
#     return res