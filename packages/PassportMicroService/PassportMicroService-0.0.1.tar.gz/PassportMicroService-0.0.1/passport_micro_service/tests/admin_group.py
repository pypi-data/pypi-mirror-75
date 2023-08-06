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
    consts.PORTAL_ADMIN_GROUP_MODIFY,
    headers,
    {
        'name': 'testgroup',
    }
)
print('PORTAL_ADMIN_GROUP_MODIFY: \n', result)

result = api_post(
    consts.PORTAL_ADMIN_GROUP_LIST,
    headers,
    {}
)
print('PORTAL_ADMIN_GROUP_LIST: \n', result)

group_uuid = result['groups'][-1]['uuid']

result = api_post(
    consts.PORTAL_ADMIN_GROUP_INFO,
    headers,
    {
        'group_uuid': group_uuid
    }
)
print('PORTAL_ADMIN_GROUP_INFO: \n', result)

result = api_post(
    consts.PORTAL_ADMIN_GROUP_DELETE,
    headers,
    {
        'group_uuid': group_uuid
    }
)
print('PORTAL_ADMIN_GROUP_DELETE: \n', result)

result = api_post(
    consts.PORTAL_ADMIN_GROUP_LIST,
    headers,
    {}
)
print('PORTAL_ADMIN_GROUP_LIST: \n', result)

result = api_post(
    consts.PORTAL_USER_LOGOUT,
    headers,
    {}
)
print('PORTAL_USER_LOGOUT: \n', result)
