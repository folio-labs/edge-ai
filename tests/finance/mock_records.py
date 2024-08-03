import pytest

@pytest.fixture
def invoice1() -> dict:
    return {
        "id": "d2f155e1-3d7f-4582-8d53-98f0ccb91375",
        "accountingCode": "40141FEEDER1",
        "adjustments": [
          {
            'id': '0c3cff1c-e330-4948-86e6-c8653fa34bba',
            'description': 'TAX',
            'exportToAccounting': True,
            'type': 'Percentage',
            'value': 5.0
          }
        ],
        "adjustmentTotal": 50.0,
        'currency': 'USD', 
        'enclosureNeeded': False,
        'exchangeRate': 1.0,
        'exportToAccounting': True,
        'folioInvoiceNo': '10129',
        'invoiceDate': '2024-08-03T00:00:00.000+00:00',
        'paymentMethod': 'Physical Check',
        'status': 'Open',
        'source': 'User',
        'subTotal': 950.64,
        'total': 1000.64,
        'vendorInvoiceNo': 'SO56383',
        'poNumbers': [],
        'vendorId': 'b5d46a78-42a7-5798-8722-9f8ee8d0ce79',
        'accountNo': '40141FEEDER1',
    }


@pytest.fixture
def order1() -> dict:
    return {
       'id': '5b90e6e6-d12e-40d2-9056-1fe428e01382',
       'approved': False,
       'approvedById': '881db1b2-7414-4e0b-880f-815cf5a812e3',
       'approvalDate': '2024-03-15T15:16:43.138+00:00',
       'billTo': 'c16a3270-0ffe-4532-a486-6f4f456f4aff',
       'dateOrdered': '2024-03-15T15:16:43.138+00:00',
       'manualPo': False,
       'notes': [],
       'poNumber': '19759',
       'orderType': 'One-Time',
       'reEncumber': False,
       'shipTo': 'c16a3270-0ffe-4532-a486-6f4f456f4aff',
       'vendor': 'b5d46a78-42a7-5798-8722-9f8ee8d0ce79',
       'workflowStatus': 'Open',
       'acqUnitIds': ['bd6c5f05-9ab3-41f7-8361-1c1e847196d3'],
    }
