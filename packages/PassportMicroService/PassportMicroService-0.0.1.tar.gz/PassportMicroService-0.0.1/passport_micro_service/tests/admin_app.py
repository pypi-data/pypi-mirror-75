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
    consts.PORTAL_ADMIN_APP_MODIFY,
    headers,
    {
        'name': 'testapp',
    }
)
print('PORTAL_ADMIN_APP_MODIFY: \n', result)

result = api_post(
    consts.PORTAL_ADMIN_APP_LIST,
    headers,
    {}
)
print('PORTAL_ADMIN_APP_LIST: \n', result)

app_uuid = result['apps'][-1]['uuid']

result = api_post(
    consts.PORTAL_ADMIN_APP_INFO,
    headers,
    {
        'app_uuid': app_uuid
    }
)
print('PORTAL_ADMIN_APP_INFO: \n', result)

result = api_post(
    consts.PORTAL_ADMIN_APP_DELETE,
    headers,
    {
        'app_uuid': app_uuid
    }
)
print('PORTAL_ADMIN_APP_DELETE: \n', result)

result = api_post(
    consts.PORTAL_ADMIN_APP_LIST,
    headers,
    {}
)
print('PORTAL_ADMIN_APP_LIST: \n', result)

result = api_post(
    consts.PORTAL_USER_LOGOUT,
    headers,
    {}
)
print('PORTAL_USER_LOGOUT: \n', result)
