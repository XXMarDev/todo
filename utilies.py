


def array_toJson(array):
    res = []
    for elemento in array:
        res.append(elemento.to_json())
    return res