import enum


MSG_REQUEST_DATA_ERROR = 'Request data error.'
MSG_XXX_SUCCESS = '%s success.'
MSG_USER_NOT_LOGIN = 'User not login.'
MSG_PLEASE_ENTER_YOUR_XXX = 'Please enter your %s!'
MSG_XXX_NOT_EXIST = 'Your %s is not exist. Please try again.'
MSG_XXX_INCORRECT = 'Your %s is incorrect. Please try again.'
MSG_XXX_USED = 'This %(names) has been used, please use other %(names) to register or login directly!'
MSG_XXX_BANNED = 'This %s has been banned!'


@enum.unique
class Msg(enum.Enum):
    # SYSTEM
    REQUEST_DATA_ERROR = -1001
    # LOGIN
    SUCCESS_LOGIN = 1001
    USER_NOT_LOGIN = 1002
    # USERNAME
    NEED_USERNAME = -1101
    INCORRECT_USERNAME = -1102
    NOTEXIST_USERNAME = -1103
    USED_USERNAME = -1104
    BANNED_USERNAME = -1105
    # USERNAME OR PASSWORD
    INCORRECT_USERNAME_OR_PASSWORD = -1106


_MESSAGES = {
    Msg.REQUEST_DATA_ERROR: lambda: MSG_REQUEST_DATA_ERROR,
    Msg.SUCCESS_LOGIN: lambda: MSG_XXX_SUCCESS % 'login',
    Msg.USER_NOT_LOGIN: lambda: MSG_USER_NOT_LOGIN,
    # USERNAME
    Msg.NEED_USERNAME: lambda: MSG_PLEASE_ENTER_YOUR_XXX % 'username',
    Msg.INCORRECT_USERNAME: lambda: MSG_XXX_INCORRECT % 'username',
    Msg.NOTEXIST_USERNAME: lambda: MSG_XXX_NOT_EXIST % 'username',
    Msg.USED_USERNAME: lambda: MSG_XXX_USED % {
        'name': 'username'
    },
    Msg.BANNED_USERNAME: lambda: MSG_XXX_BANNED % 'username',
    # USERNAME OR PASSWORD
    Msg.INCORRECT_USERNAME_OR_PASSWORD: lambda: MSG_XXX_INCORRECT % 'username or password',
}


def get_message(code):
    return code.value, _MESSAGES[code]()
