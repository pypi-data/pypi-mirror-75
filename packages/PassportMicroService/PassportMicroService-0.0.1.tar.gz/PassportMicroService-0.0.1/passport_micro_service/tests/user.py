import sys
sys.path.append('.')

from config import Config
from tests.common import post
from tests import consts


headers = {
    'X-Token': ''
}


def api_post(url_const, headers, json_data,):
    return post(
        url=url_const % (Config.DEFAULT_APP_URL,),
        json_data=json_data,
        headers=headers
    )


result = api_post(
    consts.PORTAL_USER_REGISTER,
    headers,
    {
        'username': 'testa',  # TODO: change new username before start test
        'password': '111111'
    }
)
print('PORTAL_USER_REGISTER: \n', result)

try:
    headers['X-Token'] = result['token']

    result = api_post(
        consts.PORTAL_USER_LOGOUT,
        headers,
        {}
    )
    print('PORTAL_USER_LOGOUT: \n', result)
except:
    pass

result = api_post(
    consts.PORTAL_USER_LOGIN,
    headers,
    {
        'username': 'testa',
        'password': '111111'
    }
)
print('PORTAL_USER_LOGIN: \n', result)
headers['X-Token'] = result['token']

result = api_post(
    consts.PORTAL_USER_INFO,
    headers,
    {}
)
print('PORTAL_USER_INFO: \n', result)

result = api_post(
    consts.PORTAL_USER_LOGOUT,
    headers,
    {}
)
print('PORTAL_USER_LOGOUT: \n', result)
