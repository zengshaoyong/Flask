from flask import jsonify


def Format(data):
    return \
        {
            "status": 200,
            "data": data
        }
