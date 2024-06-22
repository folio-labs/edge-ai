from typing import List

from dspy import Example

def _expand_dict(dictionary: dict, dict_inputs: list=[]) -> Example:
    example = {}
    for key, val in dictionary.items():

        match key:

            case "value":
                dict_inputs.append(key)

        match val:

            case dict():
                example[key] = _expand_dict(val)

            case list():
                example[key] = _expand_list(val)

            case str():
                example[key] = val

    if len(dict_inputs) > 0:
        return Example(**example).with_inputs(",".join(dict_inputs))
    
    return Example(**example)


def _expand_list(listing: list) -> list:
    expanded_list = []
    for row in listing:
        match row:

            case list():
                expanded_list.append(_expand_list(row))

            case dict():
                expanded_list.append(_expand_dict(row))

            case str():
                expanded_list.append(row)
                
    return expanded_list