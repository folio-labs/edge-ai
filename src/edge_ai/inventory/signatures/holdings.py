from dspy import InputField, OutputField, Signature

class CheckHoldings(Signature):
    """Verify that the holdings is based on the provided JSON record."""

    context = InputField(desc="provided JSON of Holding is assumed to be true")
    instance = InputField()
    verifies = OutputField(desc="Give a percentage between 0-100 indicating the incoming JSON holdings key-values are faithful to Holdings context key-values")
