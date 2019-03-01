errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        # 'extra': "Any extra information you want.",
    },
    'TooManyRequests': {
        'message': "TOO MANY REQUESTS.",
        'status': 429,
        # 'extra': "Any extra information you want.",
    },
    'BadRequest': {
        'message': "请输入正确的用户名和密码.",
        'status': 400,
        # 'extra': "Any extra information you want.",
    },
}
