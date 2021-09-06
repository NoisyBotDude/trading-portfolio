import time
import base64
import hmac
import hashlib
import requests

api_key = "61333947579f0d000645d73a"
api_secret = "aece8ef8-d5e2-4c59-8c0f-49f819802197"
api_passphrase = "mynameisashishsarmah"
url = 'https://api.kucoin.com/api/v1/currencies'
now = int(time.time() * 1000)
str_to_sign = str(now) + 'GET' + '/api/v1/currencies'
signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
headers = {
        'KC-API-KEY': api_key,
        'KC-API-PASSPHRASE': api_passphrase,
        'KC-API-SIGNATURE': signature,
        'KC-API-TIMESTAMP': str(now),
        'KC-API-KEY-VERSION': '1'
}

response = requests.request('get', url, headers=headers)
print(response.status_code)
print(response.json())
