import json


class StringConstant:
    """Some values in GraphQL are constants, not strings, and so they shouldn't
    be encoded or have quotes put around them. Use this to represent a constant
    and it won't be quoted in the query"""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value


def encode_list(thelist, encoder):
    for item in thelist:
        if isinstance(item, StringConstant):
            yield item.value
        else:
            yield encoder.encode(item)


def make_parameters(**kwargs):
    """Convert query parameters to the graphql format.
    This creates a formatted string of parameters and values suitable to be passed to a graphql
    mutation or query. It has a special-case for String constants (that are represented without
    quotes around them) and lists.
    String constants in a list are supported, but only to one level deep.
    This method does no validation of parameter names.

    Arguments:
         **kwargs: a mapping of field names to values
    Returns:
        A string representation of the graphql parameters
    """
    encoder = json.JSONEncoder()
    parts = []
    for k, v in kwargs.items():
        if isinstance(v, StringConstant):
            value = v.value
        elif isinstance(v, list):
            value = "[{}]".format(", ".join(item for item in encode_list(v, encoder)))
        else:
            value = encoder.encode(v)
        parts.append("{}: {}".format(k, value))
    return "\n        ".join(parts)