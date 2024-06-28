from dspy import Example

from edge_ai.utils.examples import _expand_dict, _expand_list

from folioclient import FolioClient

def _item_lookups(folio_client: FolioClient) -> dict:
    lookups = dict()
    return lookups

def _item_payload(payload):
    output = None
    match payload:

        case dict():
            output = _expand_dict(payload)

        case list():
            output = _expand_list(payload)

        case _:
            output = payload

    return output

def example(item: dict, folio_client: FolioClient) -> Example:
    expanded = {}
    lookups = _item_lookups(folio_client)
    for key, payload in item.items():

        match key:

            case _:
                expanded[key] = _item_payload(payload)

    return Example(**expanded)