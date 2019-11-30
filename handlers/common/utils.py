from inflection import underscore


def keys_to_snake(obj):
    return {underscore(key): value for key, value in obj.items()}
