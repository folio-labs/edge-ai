from dspy import ChainOfThought, Module, Prediction, Retrieve

from edge_ai.inventory.signatures.holdings import HoldingsSimilarity
from edge_ai.inventory.signatures.instance import InstanceSimilarity
from edge_ai.inventory.signatures.item import ItemSimilarity

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