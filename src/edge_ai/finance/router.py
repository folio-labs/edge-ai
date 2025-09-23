import json
import logging


from fastapi import APIRouter, File, UploadFile
from pydantic_ai import BinaryContent
from pydantic_ai.models.openai import OpenAIResponsesModel

logger = logging.getLogger(__name__)

router = APIRouter()

from edge_ai.finance.agents.invoice import (
    folio_client,
    agent as invoice_agent
)

@router.post("/finance/invoice", operation_id="invoice_upload")
async def invoice_from_pdf(pdf: UploadFile = File(...)):
    raw_pdf = pdf.file.read()
    response: dict = {}
    invoice_agent.model = OpenAIResponsesModel("gpt-4o")

    try:
        result = await invoice_agent.run(
            [BinaryContent(data=raw_pdf, media_type="application/pdf")]
        )

        response["record"] = json.loads(result.output.record)
    except Exception as error:
        response["error"] = str(error)

    return response

