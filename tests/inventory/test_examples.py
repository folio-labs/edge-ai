import pytest  # noqa

from unittest.mock import MagicMock

from edge_ai.inventory.examples.holdings import example as holdings_example
from edge_ai.inventory.examples.instance import example as instance_example
from edge_ai.inventory.examples.item import example as item_example

from .mock_records import a810372, ah810372_1, ai810372_1_1  # noqa

def mock_folio_client():
    mock = MagicMock()
    mock.contributor_types = [
        {'id': '9f0a2cf0-7a9b-45a2-a403-f68d2850d07c', 'name': 'Contributor'}
    ]
    mock.contrib_name_types = [
        {'id': '2b94c631-fca9-4892-a730-03ee529ffe2a', 'name': 'Personal name', 'ordering': '1'}
    ]

    mock.call_number_types = [
        {
            'id': '95467209-6d7b-468b-94df-0f5d7ad2747d',
            'name': 'Library of Congress classification',
            'source': 'system'
        }
    ]

    mock.locations = [
        {'id': '4573e824-9273-4f13-972f-cff7bf504217', 'name': 'Green Stacks' }
    ]

    return mock
    

def test_holdings_example(ah810372_1):  # noqa
    holdings = holdings_example(ah810372_1, mock_folio_client())

    assert holdings.hrid.startswith("ah810372_1")

def test_instance_example(a810372):  # noqa
    instance = instance_example(a810372, mock_folio_client())

    assert instance.title.startswith("Presidents and prime ministers")
    assert instance.contributors[0].contributorTypeText.startswith("Personal name")

def test_item_example(ai810372_1_1):  # noqa
    item = item_example(ai810372_1_1, mock_folio_client())

    assert item.hrid.startswith("ai810372_1_1")
