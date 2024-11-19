import base64
import json
import os

import httpx

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


async def upload_file_generation(**kwargs) -> dict:
    raw_image = kwargs["image"]
    image_format = kwargs.get("format", "image/jpeg")

    base64_image = base64.b64encode(raw_image).decode("utf-8")

    match kwargs["model"]:
        case "chatgpt":
            key = os.environ.get("OPENAI_API_KEY")
            url = "https://api.openai.com/v1/chat/completions"
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """What is the title and author of this book? Please return the result as the following JSON record:
          {"title": "Parable of the Sower", "source": "AIModel", "instanceTypeText": "text",
              "contributors": [{"name": "Octiva Butler", "contributorTypeText": "Author"}]}""",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{image_format};base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                "max_tokens": 300,
            }

        case _:
            key = None

    if key is None:
        return {"error": "Missing Model"}

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

    result = response.json()

    try:
        raw_content = result["choices"][0]["message"]["content"]
        raw_instance = raw_content.split("json\n")[-1].replace("```", "")
        output = json.loads(raw_instance)
    except json.JSONDecodeError as e:
        output = {"error": str(e)}

    return output
