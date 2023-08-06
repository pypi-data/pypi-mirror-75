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
    consts.PORTAL_USER_LOGIN,
    headers,
    {
        'username': 'admin',
        'password': '11111111'
    }
)
print('PORTAL_USER_LOGIN: \n', result)
headers['X-Token'] = result['token']

result = api_post(
    consts.PORTAL_ADMIN_USER_MODIFY,
    headers,
    {
        'username': 'testuser',
        'password': '222222',
        'permissions': [],
        'roles': ['admin'],
        'groups': [],
    }
)
print('PORTAL_ADMIN_USER_MODIFY: \n', result)

result = api_post(
    consts.PORTAL_ADMIN_USER_LIST,
    headers,
    {}
)
print('PORTAL_ADMIN_USER_LIST: \n', result)

user_uuid = result['users'][-1]['uuid']
print(result['users'][-1]['name'])

result = api_post(
    consts.PORTAL_ADMIN_USER_INFO,
    headers,
    {
        'user_uuid': user_uuid
    }
)
print('PORTAL_ADMIN_USER_INFO: \n', result)

result = api_post(
    consts.PORTAL_ADMIN_USER_MODIFY,
    headers,
    {
        'user_uuid': user_uuid,
        'username': 'testuser',
        'password': '111111',
        'permissions': [],
        'roles': ['user'],
        'groups': [],
    }
)
print('PORTAL_ADMIN_USER_MODIFY: \n', result)

result = api_post(
    consts.PORTAL_ADMIN_USER_INFO,
    headers,
    {
        'user_uuid': user_uuid
    }
)
print('PORTAL_ADMIN_USER_INFO: \n', result)

result = api_post(
    consts.PORTAL_ADMIN_USER_DELETE,
    headers,
    {
        'user_uuid': user_uuid
    }
)
print('PORTAL_ADMIN_USER_DELETE: \n', result)

result = api_post(
    consts.PORTAL_ADMIN_USER_LIST,
    headers,
    {}
)
print('PORTAL_ADMIN_USER_LIST: \n', result)

result = api_post(
    consts.PORTAL_USER_LOGOUT,
    headers,
    {}
)
print('PORTAL_USER_LOGOUT: \n', result)
