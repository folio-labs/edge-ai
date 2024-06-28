import pytest

@pytest.fixture
def a810372() -> dict:
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


@pytest.fixture
def ah810372_1()-> dict:
    return {
        'id': '5858da67-7f69-5adb-8754-f09c0f764695',
        '_version': 1,
        'hrid': 'ah810372_1',
        'holdingsTypeId': '5684e4a3-9279-4463-b6ee-20ae21bbec07',
        'formerIds': [],
        'instanceId': '0783dadd-1d5b-5ef5-8085-e5969e386c96',
        'permanentLocationId': '4573e824-9273-4f13-972f-cff7bf504217',
        'effectiveLocationId': '4573e824-9273-4f13-972f-cff7bf504217',
        'electronicAccess': [],
        'callNumberTypeId': '95467209-6d7b-468b-94df-0f5d7ad2747d',
        'callNumber': 'JF51.P68',
        'administrativeNotes': [],
        'notes': [],
        'holdingsStatements': [],
        'holdingsStatementsForIndexes': [],
        'holdingsStatementsForSupplements': [],
        'statisticalCodeIds': [],
        'holdingsItems': [],
        'bareHoldingsItems': [],
        'metadata': {
            'createdDate': '2023-08-20T23:12:13.214+00:00',
            'createdByUserId': '58d0aaf6-dcda-4d5e-92da-012e6b7dd766',
            'updatedDate': '2023-08-20T23:12:13.214+00:00',
            'updatedByUserId': '58d0aaf6-dcda-4d5e-92da-012e6b7dd766'},
        'sourceId': 'f32d531e-df79-46b3-8932-cdd35f7a2264'
    }

@pytest.fixture
def ai810372_1_1() -> dict:
    return {
        'id': 'fadf2ca8-60b6-524c-8e01-20a4c969798c',
        '_version': 1,
        'hrid': 'ai810372_1_1',
        'holdingsRecordId': '5858da67-7f69-5adb-8754-f09c0f764695',
        'formerIds': [],
        'discoverySuppress': False,
        'barcode': '36105035924245',
        'effectiveShelvingOrder': 'JF 251 P68 11',
        'effectiveCallNumberComponents': {
            'callNumber': 'JF51.P68',
            'typeId': '95467209-6d7b-468b-94df-0f5d7ad2747d'
        },
        'yearCaption': [],
        'copyNumber': '1',
        'numberOfPieces': '1',
        'administrativeNotes': [],
        'notes': [
            {
                'itemNoteTypeId': '4856cab2-91da-46b1-8e23-0af7ee0c3f41',
                'note': '910824/i:mds',
                'staffOnly': True
            }
        ],
        'circulationNotes': [],
        'status': {
            'name': 'Available',
            'date': '2023-08-20T22:53:30.990+00:00'
        },
        'materialTypeId': '1a54b431-2e4f-452d-9cae-9cee66c9a892',
        'permanentLoanTypeId': '2b94c631-fca9-4892-a730-03ee529ffe27',
        'effectiveLocationId': '4573e824-9273-4f13-972f-cff7bf504217',
        'electronicAccess': [],
        'statisticalCodeIds': [],
        'metadata': {'createdDate': '2023-08-20T23:16:13.399+00:00',
        'createdByUserId': '58d0aaf6-dcda-4d5e-92da-012e6b7dd766',
        'updatedDate': '2023-08-20T23:16:13.399+00:00',
        'updatedByUserId': '58d0aaf6-dcda-4d5e-92da-012e6b7dd766'}
  }
