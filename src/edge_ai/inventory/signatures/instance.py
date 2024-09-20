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
    instance = InputField()
    score = OutputField(
        desc="""Create a two member valid JSON hash that has instance ids and a score computing the percentage of the 
matching key-values between the incoming instance and the context:

Question: {"title": "Parable of the Sower", "source": "AIModel", "instanceTypeText": "text",
                 "contributors": [{"name": "Octiva Butler", "contributorTypeText": "Author", "contributerNameTypeText": "Personal name"}], 
                "publication": [{"publisher": "Four Walls Eight Windows", "dateOfPublication": "1993", "place": "New York"}] }}

Answer: {"3fc99be9-9801-4330-8816-167e113939c3": 20, "542ad9ed-cbcf-4b01-ad99-328e18194d3d": 45} 
"""
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
