"""
   SDC Utilities module
"""
import sys
import traceback

def extract_stack_trace() -> str:
    """Extracts full stacktrace from thown exception

    Returns:
        str: traceback of error thrown
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    stack_trace = traceback.format_exception(
        exc_type,
        exc_value,
        exc_traceback
    )
    return repr(stack_trace)

def parse_query_string_parameters(*, query_string_parameters: dict) -> dict:
    """
        Parse HTTP query string parameters into a more usable dictionary

        args:
            query_string_parameters (dict): The query string parameters from a request

        return:
            query_string_parameters (dict) : Returns the usable dictionary

    """
    parameters = {}
    for key, value in query_string_parameters.items():
        parts = key.replace(']', '').split('[')
        if len(parts) == 2:
            if not parameters.get(parts[0]):
                parameters[parts[0]] = {}
            parameters[parts[0]][parts[1]] = value
        else:
            parameters[parts[0]] = value

    return parameters


def dict_query(*, dictionary: dict, path: str, default=None):
    """
        Perform a 'dot notation' query on a dictionary

        args:
            dictionary (dict): The dictionary to query
            path (string): The dot notation query path
            default: The default value to return if key is not found

        return:
            value: Returns the value at the specified path

    """
    keys = path.split('.')
    value = None
    for key in keys:
        if value:
            if isinstance(value, list):
                if not key.isdigit():
                    return default

                value = list(value)[int(key)]
            else:
                value = value.get(key, None)
        else:
            value = dictionary.get(key, None)

        if not value:
            break

    return value if value is not None else default
