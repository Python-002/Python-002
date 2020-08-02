import requests, os
from fake_useragent import UserAgent

def login(url):
    ua = UserAgent(verify_ssl=False)
    headers = {
        'user-agent': ua.random,
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
        'referer': 'https://shimo.im/login?from=home',
        'origin': 'https://shimo.im',
        'x-requested-with': 'XmlHttpRequest'
    }

    s = requests.Session()
    #请求体
    body = {
        'email': os.getenv('mobile'),
        'mobile': '15201086598',
        'password': os.getenv('password')
    }

    #denglukaishi
    s.post(url, data=body, headers=headers)

    #session
    res = s.get('https://shimo.im/lizard-api/users/me', headers=headers)
    print(res.json())

if __name__ == '__main__':

    login('https://shimo.im/lizard-api/auth/password/login')