from dspy import InputField, OutputField, Signature

class InstanceSimilarity(Signature):
    """Verify that the instance is based on the provided JSON record."""

    context = InputField(desc="provided JSON of Instance is assumed to be true")
    instance = InputField()
    verifies = OutputField(desc="Give a percentage between 0-100 indicating how many of the key-values of the incoming JSON match to the Instance JSON key-values")
