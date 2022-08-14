import json

json_serializable = [str, int, bool, dict, list]


def _serialize_grpc_to_json(obj):
    variables = []

    for attr in dir(obj):
        if attr.islower() and attr[0] != "_":
            variables.append(attr)

    values = {variable: getattr(obj, variable) if type(getattr(obj, variable)) in json_serializable
                                               else str(getattr(obj, variable)) for variable in variables}

    return json.dumps(values)


def serialize_to_json(obj):
    if "value" not in dir(obj):
        return _serialize_grpc_to_json(obj)
    else:
        return _serialize_grpc_to_json(obj.value)
