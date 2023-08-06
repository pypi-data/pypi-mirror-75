from passport.core.messages import get_message


def api_common(data={}, code=0, message='lang.success', msg_code=None, error_field=''):
    if msg_code:
        msg = get_message(msg_code)
        response = {
            'data': data,
            'error_field': error_field,
            'code': msg[0],
            'return_message': msg[1]
        }
    else:
        response = {
            'data': data,
            'code': code,
            'return_message': message
        }
    return response
