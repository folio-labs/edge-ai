from dspy import Example

from edge_ai.utils.examples import _expand_dict, _expand_list

from folioclient import FolioClient

def _instance_lookups(folio_client: FolioClient) -> dict:
    lookups = dict()
    for types_info in [
        folio_client.contributor_types,
        folio_client.contrib_name_types
    ]:
        for row in types_info:
            lookups[row['id']] = row['name']
    return lookups


def example(instance: dict, folio_client: FolioClient) -> Example:
    expanded = {}
    lookups = _instance_lookups(folio_client)
    for key, payload in instance.items():

        match key:
            case "contributors":
                expanded[key] = []
                for contributor in payload:
                    if not contributor["contributorTypeText"]:
                        contributor["contributorTypeText"] = lookups[
                            contributor['contributorNameTypeId']
                        ]
                    expanded[key].append(_expand_dict(contributor, ["contributorTypeText", "name"]))

            case "publication":
                expanded[key] = []
                expanded[key].extend(
                    _expand_list(payload)
                )


            case _:
                match payload:

                    case dict():
                        expanded[key] = _expand_dict(payload)

                    case list():
                        expanded[key] = _expand_list(payload)

                    case _:
                        expanded[key] = payload


    return Example(**expanded).with_inputs("title", "hrid", "uuid")