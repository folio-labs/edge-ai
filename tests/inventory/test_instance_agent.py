import pytest

from pydantic_ai import models, capture_run_messages
from pydantic_ai.models.test import TestModel
from pydantic_ai.messages import (
    SystemPromptPart,
    UserPromptPart,
    ToolCallPart,
)

import edge_ai.inventory.agents.instance as instance_module
from edge_ai.inventory.agents.instance import (
    agent, 
    Dependencies, 
    FOLIOInstance,
)

models.ALLOW_MODEL_REQUESTS = False 

@pytest.fixture
def mock_folio_client(mocker):
    def mock_get(*args, **kwargs):
        match args[0]:

            case _:
                return {}
            
    mock_client = mocker.MagicMock()
    mock_client.folio_get = mock_get
    return mock_client

@pytest.mark.asyncio
async def test_generate_inventory_record(mocker, mock_folio_client):

    mocker.patch.object(instance_module,
                        "FolioClient",
                        mock_folio_client)
    
    with capture_run_messages() as messages:
        agent.model = TestModel()
        prompt = (
            "Please catalog Red Lace by Nellie Johnson published in 2023 in New York "
            "by Anytown Press"
        )
        result = await agent.run([prompt], deps=Dependencies())

    assert isinstance(messages[0].parts[0], SystemPromptPart)
    assert messages[0].parts[0].content.startswith("You are an expert cataloger")
    assert isinstance(messages[0].parts[1], UserPromptPart)
    assert messages[0].parts[1].content[0].startswith("Please catalog Red Lace")
    assert isinstance(messages[1].parts[0], ToolCallPart)
    assert messages[1].parts[0].tool_name.startswith("retrieve_reference_data")
    assert isinstance(result.output, FOLIOInstance)
    
