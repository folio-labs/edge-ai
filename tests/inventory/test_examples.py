import pytest

from unittest.mock import MagicMock

from edge_ai.inventory.examples.instance import example as instance_example

@pytest.fixture
def a810372():
    return {
        'id': '0783dadd-1d5b-5ef5-8085-e5969e386c96',
        '_version': '3',
        'hrid': 'a810372',
        'source': 'MARC',
        'title': 'Presidents and prime ministers / edited by Richard Rose and Ezra N. Suleiman.',
        'administrativeNotes': [],
        'indexTitle': 'Presidents and prime ministers',
        'parentInstances': [],
        'childInstances': [],
        'isBoundWith': False,
        'alternativeTitles': [],
        'editions': [],
        'series': [
            {
                'authorityId': None, 
                'value': 'AEI studies ; 281'
            }
        ],
        'identifiers': [
            {
                'identifierTypeId': 'c858e4f2-2b6b-4385-842b-60732ee14abb',
                'value': '80017898'
            },
            {
                'identifierTypeId': '8261054f-be78-422d-bd51-4ed9f33c3422',
                'value': '0844733865'
            },
            {
                'identifierTypeId': '8261054f-be78-422d-bd51-4ed9f33c3422',
                'value': '9780844733869'
            },
            {
                'identifierTypeId': '7e591197-f335-4afb-bc6d-a6d76ca3bace',
                'value': '(Sirsi) ADZ1767'
            },
            {
                'identifierTypeId': '7e591197-f335-4afb-bc6d-a6d76ca3bace',
                'value': '(CStRLIN)CSUG18529887-B'
            },
            {
                'identifierTypeId': '439bfbae-75bc-4f74-9fc7-b2a2d47ce3ef',
                'value': '(OCoLC-M)6446943'
            },
            {
                'identifierTypeId': '439bfbae-75bc-4f74-9fc7-b2a2d47ce3ef',
                'value': '(OCoLC-I)272078956'
            }
        ],
        'contributors': [
            {
                'authorityId': None,
                'contributorNameTypeId': '2b94c631-fca9-4892-a730-03ee529ffe2a',
                'name': 'Rose, Richard, 1933-',
                'contributorTypeId': '9f0a2cf0-7a9b-45a2-a403-f68d2850d07c',
                'contributorTypeText': None,
                'primary': False
            },
            {
                'authorityId': None,
                'contributorNameTypeId': '2b94c631-fca9-4892-a730-03ee529ffe2a',
                'name': 'Suleiman, Ezra N., 1941-',
                'contributorTypeId': '9f0a2cf0-7a9b-45a2-a403-f68d2850d07c',
                'contributorTypeText': None,
                'primary': False
            }
        ],
        'subjects': [
            {
                'authorityId': None,
                'value': 'Comparative government'
            }
        ],
        'classifications': [
            {
                'classificationNumber': 'JF51 .P68',
                'classificationTypeId': 'ce176ace-a53e-4b4d-aa89-725ed7b2edac'
            },
            {
                'classificationNumber': '351.00313',
                'classificationTypeId': '42471af9-7d25-4f3a-bf78-60d29dcf463b'
            }
        ],
        'publication': [
            {
                'publisher': 'American Enterprise Institute',
                'place': 'Washington, D.C',
                'dateOfPublication': 'c1980',
                'role': None
            }
        ],
        'publicationFrequency': [],
        'publicationRange': [],
        'electronicAccess': [],
        'instanceTypeId': '30fffe0e-e985-4144-b2e2-1e8179bdb41f',
        'instanceFormatIds': [],
        'physicalDescriptions': ['347 p. ; 23 cm.'],
        'languages': ['eng'],
        'notes': [],
        'modeOfIssuanceId': '9d18a02f-5897-4c31-9106-c9abb5c7ae8b',
        'catalogedDate': '1991-08-24',
        'previouslyHeld': False,
        'staffSuppress': False,
        'discoverySuppress': False,
        'statisticalCodeIds': [],
        'statusId': '9634a5ab-9228-4703-baf2-4d12ebc77d56',
        'statusUpdatedDate': '2023-08-20T23:08:40.393+0000',
        'metadata': {'createdDate': '2023-08-20T23:08:43.189+00:00',
        'createdByUserId': '58d0aaf6-dcda-4d5e-92da-012e6b7dd766',
        'updatedDate': '2023-08-20T23:08:43.189+00:00',
        'updatedByUserId': '58d0aaf6-dcda-4d5e-92da-012e6b7dd766'},
        'tags': {'tagList': []},
        'natureOfContentTermIds': [],
        'publicationPeriod': {'start': 1980},
        'precedingTitles': [],
        'succeedingTitles': []
    }


def mock_folio_client():
    mock = MagicMock()
    mock.contributor_types = [
        {'id': '9f0a2cf0-7a9b-45a2-a403-f68d2850d07c', 'name': 'Contributor'}
    ]
    mock.contrib_name_types = [
        {'id': '2b94c631-fca9-4892-a730-03ee529ffe2a', 'name': 'Personal name', 'ordering': '1'}
    ]

    return mock
    

def test_instance_example(a810372):
    example = instance_example(a810372, mock_folio_client())

    assert example.title.startswith("Presidents and prime ministers")
    assert example.contributors[0].contributorTypeText.startswith("Personal name")