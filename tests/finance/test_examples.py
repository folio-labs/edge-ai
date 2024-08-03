import pytest  # noqa

from unittest.mock import MagicMock

from edge_ai.finance.examples.invoice import example as invoice_example
from edge_ai.finance.examples.order import example as order_example
from .mock_records import invoice1, order1 .  # noqa


def mock_folio_client():
    def mock_folio_get(*args, **kwargs):
        output = {}
        if args[0].startswith("/finance/fiscal-years"):
            output['fiscalYears'] = [
                {
                  "id": '200bfabe-07c7-4deb-b54e-99d64a3435cb',
                  "name": "LIB2024",
                  "periodStart": "2023-08-19T07:00:00.000+00:00",
                  "periodEnd": "2024-08-31T07:00:00.000+00:00"
                }
            ]

        return output

    mock = MagicMock()

    mock.organizations = [
        {"id": "b5d46a78-42a7-5798-8722-9f8ee8d0ce79",
         "name": 'Kinokuniya Bookstores of America Co., Ltd.', 
         'code': 'KINOKUNIYAUS-SUL',
        }
    ]

    mock.folio_get = mock_folio_get
    return mock


def test_invoice_example(invoice1):
    invoice = invoice_example(invoice1, mock_folio_client())

    assert invoice.accountingCode == "40141FEEDER1"


def test_order_example(order1):
    order = order_example(order1, mock_folio_client())

    assert order.orderType == 'One-Time'
