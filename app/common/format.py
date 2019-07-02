from flask import jsonify


def Success(data):
    return jsonify({
        "CODE": 200,
        "RESULT": Format(data),
        "MESSAGE": 'SUCCESS'
    })


def Failed(data):
    if data:
        return jsonify({
            "CODE": 404,
            "ERROR": data,
            "MESSAGE": 'FAILED'
        })
    return


def Format(data):
    results = {}
    DATA = []
    if typeof(data) == 'dict':
        for k, v in data.items():
            result = {}
            result[k] = v
            DATA.append(result)
        results["PROP"] = ""
        results["DATA"] = DATA
        return results
    if typeof(data) == 'list':
        results["PROP"] = ""
        results["DATA"] = data
        return results
    return


def typeof(variate):
    type = None
    if isinstance(variate, int):
        type = "int"
    elif isinstance(variate, str):
        type = "str"
    elif isinstance(variate, float):
        type = "float"
    elif isinstance(variate, list):
        type = "list"
    elif isinstance(variate, tuple):
        type = "tuple"
    elif isinstance(variate, dict):
        type = "dict"
    elif isinstance(variate, set):
        type = "set"
    return type
