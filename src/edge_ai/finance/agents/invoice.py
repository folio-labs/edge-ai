import os

from dataclasses import dataclass
from typing import Optional, Union

from folioclient import FolioClient
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import Usage


class AIModelInfo(BaseModel):
    model_name: str
    usage: Union[dict, Usage]
    messages: list


class FOLIOInvoice(BaseModel):
    model_info: AIModelInfo
    record: Union[str, dict]


class FOLIOInvoiceLine(BaseModel):
    record: Union[str, dict]


class FOLIOPOLine(BaseModel):
    record: Union[str, dict]

folio_client = None


def _folio_client():
    global folio_client

    if not folio_client:
        folio_client = FolioClient(
            os.environ.get("GATEWAY_URL"),
            os.environ.get("TENANT_ID"),
            os.environ.get("ADMIN_USER"),
            os.environ.get("ADMIN_PASSWORD"),
        )
    return folio_client



system_instructions = "".join(
    [
        "From an uploaded Invoice PDF, create a JSON invoice with the following properties: ",
        "currency, subTotal, total, invoiceDate, batchGroupId, status, source, batchGroupId, paymentMethod, vendorInvoiceNo, vendorId. ",
        "The invoiceDate property should be formated as 'YYYY-MM-DDT00:00:00.000+0000'.",
        "Use the `batch_group_id` function to determine the batchGroupId. Use the `vendor_lookup` function ",
        "to determine the vendorId and paymentMethod properites. For the status property use 'Open' as the value and ",
        "for the source property use 'API' for the value.",
    ]
)

agent = Agent(instructions=system_instructions, output_type=FOLIOInvoice)


@agent.tool_plain
async def batch_group_id():
    batch_groups = folio_client.folio_get(
        "/batch-group-storage/batch-groups", key="batchGroups"
    )
    if len(batch_groups) > 0:
        return batch_groups[0]["id"]


@agent.tool
async def vendor_lookup(ctx: RunContext[str], vendor_name: str):
    vendor_words = vendor_name.strip().split()
    folio_client = _folio_client()
    for i in range(len(vendor_words), 0, -1):
        query_param = " ".join(vendor_words[:i])

        vendor_result = folio_client.folio_get(
            "/organizations/organizations",
            key="organizations",
            query_params={"query": f"name=={query_param}*"},
        )
        if len(vendor_result) > 0:
            vendor = vendor_result[0]
            return vendor["id"], vendor["paymentMethod"]
