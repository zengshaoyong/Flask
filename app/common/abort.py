from flask_restful import abort


class ResponseCode:
    SUCCESS = 200
    WRONG_PARAM = 400
    MESSAGE = '处理成功！'


def generate_response(data=None, message=ResponseCode.MESSAGE, status=ResponseCode.SUCCESS):
    return {
        'message': message,
        'status': status,
        'data': data
    }


def my_abort(http_status_code, *args, **kwargs):
    if http_status_code == 400:
        # 重定义400返回参数
        abort(400, **generate_response(data=[kwargs.get('message')], message='参数错误！', status=http_status_code))

    abort(http_status_code)