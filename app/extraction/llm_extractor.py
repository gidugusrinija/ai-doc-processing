import base64
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI


class MultimodalLLMExtractor:

    def __init__(self, model=None):
        self.client = OpenAI()
        self.model = model or os.getenv(
            "OPENAI_VISION_MODEL",
            "gpt-4o"
        )

    @staticmethod
    def encode_image(image_path):

        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        return f"data:image/png;base64,{encoded}"

    def extract(self, target_image, fewshot_examples):

        content = []

        content.append({
            "type": "text",
            "text": """
You are an expert medical insurance benefit document extraction system.

Extract all relevant insurance benefit information from the TARGET PAGE.

Instructions:
1. Extract information only from the target page.
2. Use the retrieved examples as guidance for output structure.
3. Do not copy values from few-shot examples.
4. Preserve numerical values, percentages, limits and conditions accurately.
5. Do not hallucinate missing information.
6. Use null when a value is unavailable.
7. Preserve the meaning of tables and structured layouts.
8. Return valid JSON only.
"""
        })

        # Add retrieved few-shot examples
        for index, example in enumerate(fewshot_examples, start=1):

            content.append({
                "type": "text",
                "text": f"""
FEW-SHOT EXAMPLE {index}

Expected extraction output:
{json.dumps(example["annotation"], indent=2)}
"""
            })

            content.append({
                "type": "image_url",
                "image_url": {
                    "url": self.encode_image(
                        example["image_path"]
                    )
                }
            })

        # Add target page
        content.append({
            "type": "text",
            "text": "TARGET PAGE: Extract information from this image."
        })

        content.append({
            "type": "image_url",
            "image_url": {
                "url": self.encode_image(target_image)
            }
        })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            response_format={
                "type": "json_object"
            },
            temperature=0,
        )

        result = response.choices[0].message.content

        return json.loads(result)