from dspy import Example

from edge_ai.utils.examples import _expand_dict, _expand_list

from folioclient import FolioClient

def _holdings_lookups(folio_client: FolioClient) -> dict:
    lookups = dict()
    for types_info in [
        folio_client.call_number_types,
        folio_client.locations
    ]:
        for row in types_info:
            lookups[row['id']] = row['name']
    return lookups

def _holdings_payload(payload):
    output = None
    match payload:

        case dict():
            output = _expand_dict(payload)

        case list():
            output = _expand_list(payload)

        case _:
            output = payload

    return output


def example(holdings: dict, folio_client: FolioClient) -> Example:
    expanded = {}
    lookups = _holdings_lookups(folio_client)
    for key, payload in holdings.items():
        match key:

            case "callNumberTypeId":
                expanded["callNumberType"] = {
                    "id": payload,
                    "name": lookups[payload] 
                }


            case "effectiveLocationId":
                expanded["effectiveLocation"] = {
                    "id": payload,
                    "name": lookups[payload]
                }


            case "permanentLocationId":
                expanded["permanentLocation"] = {
                    "id": payload,
                    "name": lookups[payload]
                }


            case _:
                expanded[key] = _holdings_payload(payload)

                
    return Example(**holdings).with_inputs('id', 'hrid', 'instanceId')