from flask import jsonify


def Format(data):
    return jsonify({
        "status": 200,
        "data": data
    })
