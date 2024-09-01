import json
import logging

from typing import Union

from dspy import ChainOfThought, Module, Prediction
from dspy.retrieve.ragatouille_rm import RAGatouilleRM

from edge_ai.inventory.signatures.holdings import HoldingsSimilarity
from edge_ai.inventory.signatures.instance import (
    InstanceSimilarity,
    InstanceSemanticSimilarity,
)
from edge_ai.inventory.signatures.item import ItemSimilarity

from ragatouille import RAGPretrainedModel

logger = logging.getLogger(__name__)


def _extract_metadata(record: dict) -> dict:
    output = {}
    if "metadata" in record:
        output = record.pop("metadata")
    output["hrid"] = record.pop("hrid")
    return output


def new_rag_index(records: list, index_name: str):
    RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
    logger.info(f"Starting indexing of {len(records):,}")
    index_path = RAG.index(
        collection=[json.dumps(record) for record in records],
        index_name=index_name,
        document_ids=[record.pop("id") for record in records],
        document_metadatas=[_extract_metadata(record) for record in records],
        split_documents=False,
    )
    logger.info(f"Finished indexing located at {index_path}")
    return index_path


def update_rag_index(records: list, index_path: str):
    RAG = RAGPretrainedModel.from_index(index_path)
    logger.info(f"Updating index {index_path} with {len(records):,} records")
    RAG.add_to_index(
        new_collection=[json.dumps(record) for record in records],
        new_document_ids=[record["id"] for record in records],
        new_document_metadatas=[{"hrid": record["hrid"]} for record in records],
        split_documents=False,
    )
    logger.info("Finished updating index.")


class Items(Module):

    def __init__(self, index_root: str, num_items=3):
        super().__init__()

        self.retrieve = RAGatouilleRM(
            index_root=index_root, index_name="Items", k=num_items
        )
        self.verified = ChainOfThought(ItemSimilarity)

    def verify(self, items: str):
        context = self.retrieve(context=context, items=items)
        predication = self.verified(context=context, items=items)

        return Prediction(
            context=context,
            rationale=predication.rationale,
            verifies=predication.verifies,
        )


class Holdings(Module):

    def __init__(self, index_root: str, num_holdings=3):
        super().__init__()

        self.retrieve = RAGatouilleRM(
            index_root=index_root, index_name="Holdings", k=num_holdings
        )
        self.verified = ChainOfThought(HoldingsSimilarity)

    def verify(self, holdings: str):
        context = self.retrieve(context=context, holdings=holdings)
        predication = self.verified(context=context, holdings=holdings)

        return Prediction(
            context=context,
            rationale=predication.rationale,
            verifies=predication.verifies,
        )


class Instances(Module):

    def __init__(self, index_root: str, num_instances=3):
        super().__init__()
        self.k = num_instances
        self.retrieve = RAGatouilleRM(
            index_root=index_root, index_name="Instances", k=num_instances
        )
        self.verified = ChainOfThought(InstanceSemanticSimilarity)

    def forward(self, operation: str, instance: str):
        context = self.retrieve(query_or_queries=instance, k=self.k).passages

        match operation:

            case "verify":
                predication = self.verified(context=context, query=instance)

            case _:
                raise ValueError(
                    f"Unknown operation {operation} for instance {instance}"
                )

        return Prediction(
            context=context,
            rationale=predication.rationale,
            verifies=predication.verifies,
        )
