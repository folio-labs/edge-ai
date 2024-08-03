from dspy import Example

from edge_ai.utils.examples import _expand_dict, _expand_list

from folioclient import FolioClient

def _invoice_lookups(client: FolioClient) -> dict:
    lookups = dict()
    for endpoint, key in [
        ("/finance/fiscal-years?limit=2000", "fiscalYears")
    ]:
        results = client.folio_get(endpoint)
        for row in results[key]:
            lookups[row['id']] = {
                "id": row['id'],
                "name": row['name']
            }
    return lookups

def _vendor_lookups(client: FolioClient) -> dict:
    vendors = dict()
    for org in client.organizations:
        vendors[org['id']] = {
            "id": org['id'],
            "name": org['name']
        }
    return vendors


def _invoice_payload(payload):
    output = None
    match payload:

        case dict():
            output = _expand_dict(payload)

        case list():
            output = _expand_list(payload)

        case _:
            output = payload

    return output

def _po_lines(po_numbers: list, vendor_lookup: dict, client: FolioClient) -> list:
    purchase_orders = []
    for number in po_numbers:
        purchase_order_result = client.folio_get(f"/orders/composite-orders?query=(poNumber=={number}")
        if len(purchase_order_result["purchaseOrders"]) > 0:
            # Use the first purchase order
            po = purchase_order_result["purchaseOrders"][0]
            expanded = dict()
            for key, value in po.items():
                match key:

                    case "vendor":
                        expanded[key] = vendor_lookup[value]

                    case _:
                        expanded[key] = _invoice_payload(value)

            purchase_orders.append(
                Example(**expanded)
            )
    return purchase_orders



def example(invoice: dict, folio_client: FolioClient) -> Example:
    expanded = {}
    lookups = _invoice_lookups(folio_client)
    vendors = _vendor_lookups(folio_client)
    for key, payload in invoice.items():

        match key:

            case "fiscalYearId":
                expanded["fiscalYear"] = lookups[payload]

            case "poLines":
                expanded[key] = _po_lines(payload, vendors, folio_client)

            case "vendorId":
                expanded[key] = vendors[payload]

            case _:
                expanded[key] = _invoice_payload(payload)

    return Example(**expanded)
