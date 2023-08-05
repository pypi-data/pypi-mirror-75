def replace_str(data):
    """
    Function to recursively traverse a json data structure and
    replace strings with double quotes.

    Parameters
    ==========
    data: json data structure

    Returns
    =======
    data: updated json
    """
    if isinstance(data, dict):
        return {k: replace_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_str(i) for i in data]
    else:
        return '"{}"'.format(data) if isinstance(data, str) else data


def dict_to_query_str(dict_object):
    """
    Converts a dictionary object to Graphql string.
    """
    input_str = str(dict_object)
    input_str = input_str.replace("'", "")
    while input_str.count("{") != input_str.count("}"):
        if input_str.count("{") > input_str.count("}"):
            input_str += "}"
        else:
            input_str.insert(0, "{")
    return input_str


def dict_to_arg_str(args):
    """
    Converts an arguments dictionary object to Graphql argument string.
    """
    args = replace_str(args)
    input_str = "("
    for i, k in enumerate(args):
        if i > 0:
            input_str += ","
        if isinstance(args[k], dict):
            sub_str = dict_to_query_str(args[k])
            input_str += str(k) + ": " + sub_str
        else:
            if isinstance(args[k], str):
                input_str += str(k) + ":" + args[k]
            else:
                input_str += str(k) + ":" + str(args[k])
    input_str += ")"
    return input_str
