"""Dataclass to json conversion"""

__author__ = "Wytze Bruinsma"


def rec_to_json(objects):
    """
    Recursive function that can make a json from complex nested objects

    :param objects:
    :return:
    """

    if not hasattr(objects, "__dict__"):
        return objects
    result = {}
    for key, val in objects.__dict__.items():
        if key.startswith("_"):
            continue
        element = []
        if isinstance(val, list):
            for item in val:
                element.append(rec_to_json(item))
        else:
            element = rec_to_json(val)
        result[key] = element
    return result
