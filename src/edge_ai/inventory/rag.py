import json
import logging

from dspy import ChainOfThought, Module, Prediction, Retrieve

from edge_ai.inventory.signatures.holdings import HoldingsSimilarity
from edge_ai.inventory.signatures.instance import InstanceSimilarity
from edge_ai.inventory.signatures.item import ItemSimilarity

from ragatouille import RAGPretrainedModel

logger = logging.getLogger(__name__)

async def new_rag_index(records: list, index_name: str):
    RAG = RAGPretrainedModel.from_pretrained(
            "colbert-ir/colbertv2.0")
    logger.info(f"Starting indexing of {len(records):,}")
    index_path = RAG.index(
        collection=[json.dumps(record) for record in records],
        index_name=index_name,
        document_ids=[record['id'] for record in records],
        document_metadatas=[{"hrid": record['hrid']} for record in records],
        split_documents=False
    )
    logger.info(f"Finished indexing located at {index_path}")
    return index_path


async def update_rag_index(records: list, index_path: str):
    RAG = RAGPretrainedModel.from_index(index_path)
    logger.info(f"Updating index {index_path} with {len(records):,} records")
    RAG.add_to_index(
        new_collection=[json.dumps(record) for record in records],
        new_document_ids=[record['id'] for record in records],
        new_document_metadatas=[{"hrid": record['hrid']} for record in records],
        split_documents=False
    )
    logger.info("Finished updating index.")


class Items(Module):

    def __init__(self, num_items=3):
        super().__init__()

        self.retrieve = Retrieve(k=num_items)
        self.verified = ChainOfThought(ItemSimilarity)

    def verify(self, items: str):
        context = self.retrieve(context=context, items=items)
        predication = self.verified(context=context, items=items)
         
        return Prediction(
                context=context,
                rationale=predication.rationale,
                verifies=predication.verifies
            )


class Holdings(Module):

    def __init__(self, num_holdings=3):
        super().__init__()

        self.retrieve = Retrieve(k=num_holdings)
        self.verified = ChainOfThought(HoldingsSimilarity)

    def verify(self, holdings: str):
         context = self.retrieve(context=context, holdings=holdings)
         predication = self.verified(context=context, holdings=holdings)

         return Prediction(
             context=context,
             rationale=predication.rationale,
             verifies=predication.verifies
        )


class Instances(Module):

    def __init__(self, num_instances=3):
        super().__init__()

        self.retrieve = Retrieve(k=num_instances)
        self.verified = ChainOfThought(InstanceSimilarity)

    def forward(self, operation: str, instance: str):
        context = self.retrieve(instance=instance).passages

        match operation:

            case "verify":
                predication = self.verified(context=context, instance=instance)

            case _:
                raise ValueError(f"Unknown operation {operation} for instance {instance}")

        return Prediction(
             context=context,
             rationale=predication.rationale,
             verifies=predication.verifies
        )
