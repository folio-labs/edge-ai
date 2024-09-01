from dspy import InputField, OutputField, Signature


class InstanceSimilarity(Signature):
    """Verify that the instance is based on the provided JSON record."""

    context = InputField(desc="provided JSON of Instance is assumed to be true")
    instance = InputField()
    verifies = OutputField(
        desc="Give a percentage between 0-100 indicating how many of the key-values of the incoming JSON match to the Instance JSON key-values"
    )

class InstanceSemanticSimilarity(Signature):
    context = InputField()
    verifies = OutputField(
       desc="Return the id of any FOLIO Instance that matches has a score of at least 120"
    )

class InstancePromptGeneration(Signature):
    """Generates an instance JSON record based on prompt"""

    prompt = InputField(
        desc="""You are an expert cataloger, you will create a JSON record based on question:
           Question: Parable of the Sower by Octiva Butler, published in 1993 by Four Walls Eight Windows in New York

           Answer: {"title": "Parable of the Sower", "source": "AIModel", "instanceTypeText": "text",
                 "contributors": [{"name": "Octiva Butler", "contributorTypeText": "Author"}], 
                "publication": [{"publisher": "Four Walls Eight Windows", "dateOfPublication": "1993", "place": "New York"}] }}"""
    )
    instance = OutputField(desc="Return any records as FOLIO JSON")
