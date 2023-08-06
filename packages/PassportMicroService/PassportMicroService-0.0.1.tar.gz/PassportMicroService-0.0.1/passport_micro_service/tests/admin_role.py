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
    consts.PORTAL_ADMIN_ROLE_MODIFY,
    headers,
    {
        'name': 'testrole',
    }
)
print('PORTAL_ADMIN_ROLE_MODIFY: \n', result)

result = api_post(
    consts.PORTAL_ADMIN_ROLE_LIST,
    headers,
    {}
)
print('PORTAL_ADMIN_ROLE_LIST: \n', result)

role_uuid = result['roles'][-1]['uuid']

result = api_post(
    consts.PORTAL_ADMIN_ROLE_INFO,
    headers,
    {
        'role_uuid': role_uuid
    }
)
print('PORTAL_ADMIN_ROLE_INFO: \n', result)

result = api_post(
    consts.PORTAL_ADMIN_ROLE_DELETE,
    headers,
    {
        'role_uuid': role_uuid
    }
)
print('PORTAL_ADMIN_ROLE_DELETE: \n', result)

result = api_post(
    consts.PORTAL_ADMIN_ROLE_LIST,
    headers,
    {}
)
print('PORTAL_ADMIN_ROLE_LIST: \n', result)

result = api_post(
    consts.PORTAL_USER_LOGOUT,
    headers,
    {}
)
print('PORTAL_USER_LOGOUT: \n', result)
