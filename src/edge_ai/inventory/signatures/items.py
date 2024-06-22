from dspy import InputField, OutputField, Signature

class CheckItem(Signature):
    """Verify that the items is based on the provided JSON record."""

    context = InputField(desc="provided JSON of Item is assumed to be true")
    instance = InputField()
    verifies = OutputField(desc="True or False indicating the incoming JSON is faithful to Items JSON")
