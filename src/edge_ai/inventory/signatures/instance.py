from dspy import InputField, OutputField, Signature

class CheckInstance(Signature):
    """Verify that the instance is based on the provided JSON record."""

    context = InputField(desc="provided JSON of Instance is assumed to be true")
    instance = InputField()
    verifies = OutputField(desc="Give a percentage 0-100 indicating how the incoming JSON is faithful to Instance JSON")
