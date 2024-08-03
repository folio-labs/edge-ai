from dspy import Example

from edge_ai.utils.examples import _expand_dict, _expand_list

from folioclient import FolioClient

def _vendor_lookups(client: FolioClient) -> dict:
    vendors = dict()
    for org in client.organizations:
        vendors[org['id']] = {
            "id": org['id'],
            "name": org['name']
        }
    return vendors


def _order_payload(payload):
    output = None
    match payload:

        case dict():
            output = _expand_dict(payload)

        case list():
            output = _expand_list(payload)

        case _:
            output = payload

    return output


def example(order: dict, folio_client: FolioClient) -> Example:
    expanded = {}
    vendors = _vendor_lookups(folio_client)

    for key, payload in order.items():
        
        match key:


            case "vendor":
                expanded[key] = vendors[payload]
        
            case _:
                expanded[key] = _order_payload(payload)

    return Example(**expanded)        


