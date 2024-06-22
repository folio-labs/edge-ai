import json

import dspy

from dspy import ChainOfThought
from dspy.utils.dummies import DummyLM

from edge_ai.inventory.signatures.holdings import CheckHoldings
from edge_ai.inventory.signatures.instance import CheckInstance
from edge_ai.inventory.signatures.items import CheckItem


def test_check_holdings_uuid():

    lm = DummyLM({
        "rationale": "No matching between holdings context and holdings",
        "verifies": "0%"
    })

    dspy.settings.configure(lm=lm)

    cot = ChainOfThought(CheckHoldings)

    predication = cot(context="{}", holdings=json.dumps({ "id": "ef88a6a1-e95f-49a4-99c0-40656302a055" }))

    assert predication.verifies == "0%"


def test_check_instance_uuid():
    lm = DummyLM({
        "rationale": "No matching between instance context and instance",
        "verifies": "0%"
    })

    dspy.settings.configure(lm=lm)

    cot = ChainOfThought(CheckInstance)

    predication = cot(context="{}", instance=json.dumps({ "id": "5c93512d-401c-4f68-baca-0f53a2a449d3"}))

    assert predication.verifies == "0%"


def test_check_item_uuid():
    lm = DummyLM({
        "rationale": "No matching between item context and item",
        "verifies": "0%"
    })

    dspy.settings.configure(lm=lm)

    cot = ChainOfThought(CheckItem)

    predication = cot(context="{}", item=json.dumps({ "id": "8c20dfdc-645b-499e-b969-320beb5069ea"}))

    assert predication.verifies == "0%"

