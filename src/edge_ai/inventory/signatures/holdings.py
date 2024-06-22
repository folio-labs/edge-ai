from dspy import InputField, OutputField, Signature

class CheckHoldings(Signature):
    """Verify that the holdings is based on the provided JSON record."""

    context = InputField(desc="provided JSON of Holding is assumed to be true")
    instance = InputField()
    verifies = OutputField(desc="True or False indicating the incoming JSON is faithful to Holdings JSON")
