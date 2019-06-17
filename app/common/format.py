from flask import jsonify


def Success(data):
    return jsonify({
        "status": 200,
        "data": data,
        "message": 'SUCCESS'
    })

def Failed(data):
    return jsonify({
        "status": 200,
        "data": data,
        "message": 'FAILED'
    })
